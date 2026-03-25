# NYC Places Recommendation System

A recommendation engine that suggests NYC places to visit based on user interests and demographics, powered by HuggingFace transformers.

## Features

- 🤖 Uses HuggingFace `sentence-transformers` for semantic similarity matching
- 🎯 Intelligent matching of user preferences with place characteristics
- 🚀 Interactive Gradio web interface + RESTful API
- 💾 SQLite database for portable, embedded data storage
- 💰 Price tier filtering system ($, $$, $$$, $$$$)
- 🏷️ Category-based filtering (Cafe, Food, Entertainment, Museums, etc.)
- 👤 Solo/Group friendly filtering
- 📊 139 curated NYC locations across all boroughs

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup

**The SQLite database (`nyc_places.db`) is included in the repository** - no setup needed!

If you need to recreate it from CSV files:
```bash
python create_database.py
```

### 3. Run the Application

**Gradio Web Interface** (recommended):
```bash
python app.py
```
Then open your browser to the URL shown (usually `http://127.0.0.1:7860`)

**Flask REST API** (for developers):
```bash
python flask_api.py
```
The API server will start at `http://localhost:5000`

## API Endpoints

### Get Recommendations

**POST** `/api/recommendations`

Request body with all available filters:
```json
{
  "preferred_neighborhood": "Manhattan",
  "activities": "Eating, Museums",
  "dining_preferences": "Fine Dining, Rooftop",
  "atmosphere": "Lively & Social",
  "music_genres": "Hip-Hop, Jazz",
  "activity_type": "Both",
  "drinks": true,
  "price_tier": "$$",
  "max_price_tier": "$$",
  "solo_friendly": true,
  "group_friendly": true,
  "category": "Cafe",
  "top_n": 10
}
```

### Get User-Specific Recommendations

**GET** `/api/user/<user_id>/recommendations?top_n=10`

### Get All Places

**GET** `/api/places`

### Get Place Details

**GET** `/api/places/<place_id>`

## Available Filters

### Semantic Matching (influences similarity score)
- **`preferred_neighborhood`**: String - Preferred NYC area (e.g., "Manhattan", "Brooklyn")
- **`activities`**: String - Favorite activities (e.g., "Eating, Museums, Art")
- **`dining_preferences`**: String - Dining style (e.g., "Fine Dining, Rooftop")
- **`atmosphere`**: String - Vibe preference (e.g., "Lively & Social", "Quiet & Relaxed")
- **`music_genres`**: String - Music preferences (e.g., "Hip-Hop, Jazz, R&B")
- **`activity_type`**: String - "Solo", "Group", or "Both"
- **`drinks`**: Boolean - Whether user drinks socially

### Hard Filters (exclude non-matching places)
- **`price_tier`**: String or Array - Specific tier(s): `"$$"` or `["$$", "$$$"]`
  - `$` = Under $15
  - `$$` = $15-$40
  - `$$$` = $41-$80
  - `$$$$` = Over $80
- **`max_price_tier`**: String - Maximum price tier (includes all tiers below)
- **`solo_friendly`**: Boolean - Only show solo-friendly places
- **`group_friendly`**: Boolean - Only show group-friendly places
- **`category`**: String or Array - Filter by category: `"Cafe"` or `["Cafe", "Entertainment"]`
  - Available: Food, Museum, Cafe, Entertainment, Night Life, Bar, Gallery, Activity, Cocktail Lounge

## How It Works

1. **Data Processing**: Converts place attributes (type, vibe, neighborhood, etc.) into text
2. **Embeddings**: Uses HuggingFace's `all-MiniLM-L6-v2` model to generate semantic embeddings
3. **Similarity Matching**: Calculates cosine similarity between user preferences and place embeddings
4. **Ranking**: Returns top-N places with highest similarity scores

## Example Usage

### Basic Usage
```python
from recommendation_engine import NYCRecommendationEngine

engine = NYCRecommendationEngine()

user_profile = {
    'preferred_neighborhood': 'Manhattan',
    'activities': 'Eating, Museums',
    'atmosphere': 'Lively & Social',
    'drinks': True
}

recommendations = engine.get_recommendations(user_profile, top_n=5)
print(recommendations)
```

### Advanced Usage with Filters
```python
# Budget-conscious solo cafe explorer
user_profile = {
    'preferred_neighborhood': 'Brooklyn',
    'activities': 'Coffee, Reading, Working',
    'atmosphere': 'Quiet & Relaxed',
    'category': 'Cafe',
    'solo_friendly': True,
    'max_price_tier': '$'
}

recommendations = engine.get_recommendations(user_profile, top_n=10)

# Group nightlife with price range
user_profile = {
    'preferred_neighborhood': 'Manhattan',
    'activities': 'Dancing, Music',
    'atmosphere': 'Energetic',
    'music_genres': 'Hip-Hop, House',
    'category': 'Night Life',
    'group_friendly': True,
    'price_tier': ['$$', '$$$'],
    'drinks': True
}

recommendations = engine.get_recommendations(user_profile, top_n=10)
```

## Tech Stack

- **Python 3.x**
- **HuggingFace Transformers**: For embeddings and semantic similarity
- **Flask**: REST API framework
- **Pandas**: Data manipulation
- **scikit-learn**: Cosine similarity calculations

## Testing

Run the included test scripts to verify functionality:

```bash
# Test basic recommendation engine
python test_recommendations.py

# Test price tier filtering
python test_price_tiers.py

# Test solo/group and category filters
python test_new_filters.py
```

## Dataset

The system uses a **SQLite database** (`nyc_places.db`) containing:

- **Users table**: 92 user profiles with preferences, demographics, and interests
- **Places table**: 139 NYC locations with attributes including:
  - Type, Category, Neighborhood
  - Vibe and Crowd Type
  - Price Level, Solo/Group Friendliness
  - Music, Alcohol, and Smoking availability

**CSV files** (`Users.csv` and `Places.csv`) are also included for reference and can be used to recreate the database.

## Future Enhancements

- Implement user feedback loop for better recommendations
- Add collaborative filtering based on similar users
- Integrate geolocation and travel time calculations
- Build interactive frontend application
- Deploy to cloud platform (Heroku, AWS, GCP)
- Add more NYC locations to the database
