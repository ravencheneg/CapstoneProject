import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import os
import re
import warnings
warnings.filterwarnings('ignore')


class NYCRecommendationEngine:
    """
    Recommendation engine for NYC places using HuggingFace embeddings.
    Uses user preferences and demographics to suggest places to visit.
    """

    def __init__(self, db_path='nyc_places.db'):
        """
        Initialize the recommendation engine with SQLite database.

        Args:
            db_path: Path to SQLite database file (default: 'nyc_places.db')
        """
        # Check if database exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' not found. Run create_database.py first.")

        # Load data from SQLite database
        print(f"Loading data from {db_path}...")
        conn = sqlite3.connect(db_path)
        self.users_df = pd.read_sql_query("SELECT * FROM users", conn)
        self.places_df = pd.read_sql_query("SELECT * FROM places", conn)
        conn.close()
        print(f"Loaded {len(self.users_df)} users and {len(self.places_df)} places")

        # Load HuggingFace sentence transformer model for semantic similarity
        print("Loading HuggingFace model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully!")

        self.place_embeddings = None
        self.process_data()

    def process_data(self):
        """Process and prepare data for recommendations."""
        # Convert price levels to tier system ($, $$, $$$, $$$$)
        self.places_df['price_tier'] = self.places_df['Price_Level'].apply(
            self._convert_to_price_tier
        )

        # Create text representations for places
        self.places_df['text_representation'] = self._create_place_text()

        # Generate embeddings for all places
        print("Generating embeddings for places...")
        self.place_embeddings = self.model.encode(
            self.places_df['text_representation'].tolist(),
            show_progress_bar=True
        )
        print(f"Generated embeddings for {len(self.place_embeddings)} places")

    def _convert_to_price_tier(self, price_str):
        """
        Convert price string to tier system ($, $$, $$$, $$$$).

        Price tiers:
        - $ : Under $15
        - $$ : $15-$40
        - $$$ : $41-$80
        - $$$$ : Over $80

        Args:
            price_str: String like "$5–$20 per person", "$25 per person", or empty

        Returns:
            str: Price tier ("$", "$$", "$$$", "$$$$") or None if unparseable
        """
        if pd.isna(price_str) or price_str == '':
            return None

        # Extract all numbers from the price string
        numbers = re.findall(r'\$?(\d+)', str(price_str))

        if not numbers:
            return None

        # Convert to integers and get the average or max price
        prices = [int(n) for n in numbers]
        avg_price = sum(prices) / len(prices)

        # Categorize into tiers
        if avg_price < 15:
            return "$"
        elif avg_price < 40:
            return "$$"
        elif avg_price < 80:
            return "$$$"
        else:
            return "$$$$"

    def _create_place_text(self):
        """Create textual representation of places for embedding."""
        texts = []
        for _, place in self.places_df.iterrows():
            parts = [
                f"Type: {place['Type']}",
                f"Category: {place['Category']}",
                f"Neighborhood: {place['Neighborhood']}",
                f"Vibe: {place['Vibe_Type']}",
                f"Crowd: {place['Crowd_Type']}",
            ]

            # Add features
            if place['Has_Music'] == 'Yes':
                parts.append("Has music")
            if place['Has_Alcohol'] == 'Yes':
                parts.append("Serves alcohol")
            if place['Solo_Friendly'] == 'Yes':
                parts.append("Solo friendly")
            if place['Group_Friendly'] == 'Yes':
                parts.append("Group friendly")

            texts.append('. '.join(parts))

        return texts

    def _create_user_profile(self, user_data):
        """Create a textual representation of user preferences."""
        parts = []

        # Preferred neighborhood
        if 'preferred_neighborhood' in user_data:
            parts.append(f"Prefers {user_data['preferred_neighborhood']}")

        # Activities
        if 'activities' in user_data:
            parts.append(f"Enjoys {user_data['activities']}")

        # Dining preferences
        if 'dining_preferences' in user_data:
            parts.append(f"Dining: {user_data['dining_preferences']}")

        # Atmosphere
        if 'atmosphere' in user_data:
            parts.append(f"Atmosphere: {user_data['atmosphere']}")

        # Music preferences
        if 'music_genres' in user_data:
            parts.append(f"Music: {user_data['music_genres']}")

        # Solo or group
        if 'activity_type' in user_data:
            if user_data['activity_type'] == 'Solo':
                parts.append("Solo friendly")
            elif user_data['activity_type'] == 'Group':
                parts.append("Group friendly")
            else:
                parts.append("Solo and group friendly")

        # Drinking/smoking
        if user_data.get('drinks', False):
            parts.append("Serves alcohol")

        return '. '.join(parts)

    def get_recommendations(self, user_data, top_n=10):
        """
        Get top N recommendations for a user based on their profile.

        Args:
            user_data (dict): Dictionary containing user preferences
            top_n (int): Number of recommendations to return

        Returns:
            pd.DataFrame: Top recommended places with similarity scores
        """
        # Create user profile text
        user_profile_text = self._create_user_profile(user_data)

        # Generate embedding for user profile
        user_embedding = self.model.encode([user_profile_text])

        # Calculate cosine similarity between user and all places
        similarities = cosine_similarity(user_embedding, self.place_embeddings)[0]

        # Add similarity scores to dataframe
        results = self.places_df.copy()
        results['similarity_score'] = similarities

        # Apply price tier filter if specified
        if 'price_tier' in user_data and user_data['price_tier'] is not None:
            # Filter by price tier(s)
            # User can specify single tier like "$" or multiple like ["$", "$$"]
            price_tier = user_data['price_tier']

            if isinstance(price_tier, str):
                # Single tier specified
                results = results[
                    (results['price_tier'].isna()) |
                    (results['price_tier'] == price_tier)
                ]
            elif isinstance(price_tier, list):
                # Multiple tiers specified
                results = results[
                    (results['price_tier'].isna()) |
                    (results['price_tier'].isin(price_tier))
                ]

        if 'max_price_tier' in user_data and user_data['max_price_tier'] is not None:
            # Filter by maximum price tier
            # E.g., "$$" means include only "$" and "$$"
            tier_order = ["$", "$$", "$$$", "$$$$"]
            max_tier = user_data['max_price_tier']

            if max_tier in tier_order:
                max_index = tier_order.index(max_tier)
                allowed_tiers = tier_order[:max_index + 1]
                results = results[
                    (results['price_tier'].isna()) |
                    (results['price_tier'].isin(allowed_tiers))
                ]

        # Apply Solo/Group Friendly filter
        if 'solo_friendly' in user_data and user_data['solo_friendly'] is True:
            # Filter for solo-friendly places only
            results = results[results['Solo_Friendly'] == 'Yes']

        if 'group_friendly' in user_data and user_data['group_friendly'] is True:
            # Filter for group-friendly places only
            results = results[results['Group_Friendly'] == 'Yes']

        # Apply Category filter
        if 'category' in user_data and user_data['category'] is not None:
            # Filter by category or list of categories
            category = user_data['category']

            if isinstance(category, str):
                # Single category specified
                results = results[results['Category'] == category]
            elif isinstance(category, list):
                # Multiple categories specified
                results = results[results['Category'].isin(category)]

        # Sort by similarity and return top N
        recommendations = results.nlargest(top_n, 'similarity_score')

        return recommendations[[
            'Name_of_place', 'Type', 'Category', 'Neighborhood',
            'Address', 'Vibe_Type', 'price_tier', 'Price_Level', 'similarity_score'
        ]]

    def get_user_by_id(self, user_id):
        """Retrieve user data from the Users.csv by ID."""
        user_row = self.users_df[self.users_df['#'] == user_id]
        if user_row.empty:
            return None

        user = user_row.iloc[0]
        return {
            'name': f"{user['What is your First Name?']} {user['What is your Last Name?']}",
            'preferred_neighborhood': user['What part of New York do you prefer to hang out in?'],
            'activities': user['What are your favorite activities to do in New York?'],
            'dining_preferences': user['Please rank your preferred dining experience'],
            'atmosphere': user['What kind of atmosphere do you prefer?'],
            'activity_type': user['Do you usually do solo or group activities?'],
            'drinks': user['Do you drink socially?'] == 'Yes'
        }


def main():
    """Example usage of the recommendation engine."""
    # Initialize the engine
    engine = NYCRecommendationEngine()

    # Example: Get recommendations for a custom user profile
    user_profile = {
        'preferred_neighborhood': 'Manhattan',
        'activities': 'Eating, Museums, Art Galleries',
        'dining_preferences': 'Fine Dining, Rooftop',
        'atmosphere': 'Lively & Social',
        'music_genres': 'Hip-Hop, R&B, Jazz',
        'activity_type': 'Both',
        'drinks': True
    }

    print("\n" + "="*60)
    print("NYC PLACE RECOMMENDATIONS")
    print("="*60)

    recommendations = engine.get_recommendations(user_profile, top_n=10)

    print("\nTop 10 Recommendations:")
    print("-"*60)
    for idx, row in recommendations.iterrows():
        print(f"\n{row['Name_of_place']}")
        print(f"  Type: {row['Type']}")
        print(f"  Neighborhood: {row['Neighborhood']}")
        print(f"  Vibe: {row['Vibe_Type']}")
        print(f"  Price: {row['Price_Level']}")
        print(f"  Match Score: {row['similarity_score']:.3f}")


if __name__ == "__main__":
    main()
