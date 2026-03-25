"""
Quick test to verify SQLite database works with recommendation engine.
"""
from recommendation_engine import NYCRecommendationEngine

print("Testing SQLite database integration...")
print("="*60)

# Initialize engine with SQLite database
engine = NYCRecommendationEngine(db_path='nyc_places.db')

# Test recommendation
user_profile = {
    'preferred_neighborhood': 'Manhattan',
    'activities': 'Eating, Museums',
    'atmosphere': 'Lively & Social',
    'category': 'Food',
    'max_price_tier': '$$'
}

print("\nGetting recommendations...")
recommendations = engine.get_recommendations(user_profile, top_n=3)

print("\nTop 3 Recommendations:")
print("="*60)
for idx, row in recommendations.iterrows():
    print(f"\n{row['Name_of_place']}")
    print(f"  Type: {row['Type']} | Neighborhood: {row['Neighborhood']}")
    print(f"  Price: {row['price_tier']} | Match: {row['similarity_score']:.1%}")

print("\n" + "="*60)
print("✅ Database integration successful!")
