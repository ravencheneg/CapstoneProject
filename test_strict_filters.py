"""
Test the new strict filtering behavior - all preferences now work as filters.
"""
from recommendation_engine import NYCRecommendationEngine

print("Testing STRICT FILTERING for All Preferences")
print("="*70)

engine = NYCRecommendationEngine()

# TEST 1: Neighborhood filter - should only show Upper East Side
print("\nTEST 1: Neighborhood Filter = 'Upper East Side'")
print("="*70)

user_data = {
    'preferred_neighborhood': 'Upper East Side'
}

recs = engine.get_recommendations(user_data, top_n=10)
print(f"Found {len(recs)} recommendations")

neighborhoods = recs['Neighborhood'].unique()
print(f"\nNeighborhoods in results: {neighborhoods}")

if len(neighborhoods) == 1 and neighborhoods[0] == 'Upper East Side':
    print("✅ PASS - Only Upper East Side places shown")
else:
    print(f"❌ FAIL - Found other neighborhoods: {neighborhoods}")

print("\nSample results:")
for idx, row in recs.head(5).iterrows():
    print(f"  {row['Name_of_place']:40} | {row['Neighborhood']}")

# TEST 2: Upscale + Upper East Side
print("\n" + "="*70)
print("TEST 2: Neighborhood='Upper East Side' + Atmosphere='Upscale'")
print("="*70)

user_data = {
    'preferred_neighborhood': 'Upper East Side',
    'atmosphere': 'Upscale'
}

recs = engine.get_recommendations(user_data, top_n=10)
print(f"Found {len(recs)} recommendations")

print("\nAll results:")
for idx, row in recs.iterrows():
    neighborhood_match = "✅" if row['Neighborhood'] == 'Upper East Side' else "❌"
    upscale_match = "✅" if 'upscale' in str(row['Vibe_Type']).lower() else "❌"

    print(f"{neighborhood_match} {upscale_match} {row['Name_of_place']:35} | {row['Neighborhood']:20} | {row['Vibe_Type']}")

# TEST 3: Category filter
print("\n" + "="*70)
print("TEST 3: Category='Cafe' in Brooklyn")
print("="*70)

user_data = {
    'preferred_neighborhood': 'Brooklyn',
    'category': 'Cafe'
}

recs = engine.get_recommendations(user_data, top_n=10)
print(f"Found {len(recs)} recommendations")

categories = recs['Category'].unique()
neighborhoods = recs['Neighborhood'].unique()

print(f"\nCategories: {categories}")
print(f"Neighborhoods: {neighborhoods}")

if all(cat == 'Cafe' for cat in categories) and all(n == 'Brooklyn' for n in neighborhoods):
    print("✅ PASS - Only Brooklyn cafes shown")
else:
    print("❌ FAIL - Found non-matching results")

print("\nSample results:")
for idx, row in recs.head(5).iterrows():
    print(f"  {row['Name_of_place']:40} | {row['Category']:15} | {row['Neighborhood']}")

# TEST 4: Activity Type filter
print("\n" + "="*70)
print("TEST 4: Activity Type='Solo'")
print("="*70)

user_data = {
    'activity_type': 'Solo',
    'max_price_tier': '$$'
}

recs = engine.get_recommendations(user_data, top_n=10)
print(f"Found {len(recs)} recommendations")

# Check if all are solo-friendly (data would need Solo_Friendly column)
print("\nSample results (all should be solo-friendly):")
for idx, row in recs.head(5).iterrows():
    print(f"  {row['Name_of_place']:40} | {row['Category']}")

# TEST 5: Multiple filters combined
print("\n" + "="*70)
print("TEST 5: Manhattan + Upscale + Food + $$$")
print("="*70)

user_data = {
    'preferred_neighborhood': 'Manhattan',
    'atmosphere': 'Upscale',
    'category': 'Food',
    'max_price_tier': '$$$'
}

recs = engine.get_recommendations(user_data, top_n=10)
print(f"Found {len(recs)} recommendations")

print("\nAll results:")
for idx, row in recs.iterrows():
    print(f"  {row['Name_of_place']:35} | {row['Neighborhood']:15} | {row['Vibe_Type']:20} | {row['price_tier']}")

print("\n" + "="*70)
print("✅ All strict filtering tests completed!")
print("="*70)
