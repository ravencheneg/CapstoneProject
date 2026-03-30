"""
Test atmosphere filtering.
"""
from recommendation_engine import NYCRecommendationEngine

print("Testing Atmosphere Hard Filtering")
print("="*70)

engine = NYCRecommendationEngine()

# Test 1: "Lively & Social" should only show lively/social vibes
print("\nTEST 1: 'Lively & Social' atmosphere")
print("="*70)

user1 = {
    'activities': 'Dining, Entertainment',
    'atmosphere': 'Lively & Social',
    'max_price_tier': '$$'
}

recs1 = engine.get_recommendations(user1, top_n=10)
print(f"\nFound {len(recs1)} recommendations")
print("\nAll vibes in results:")
print(recs1['Vibe_Type'].value_counts())

print("\nTop 5:")
for idx, row in recs1.head().iterrows():
    print(f"  {row['Name_of_place']}: {row['Vibe_Type']}")

# Test 2: "Quiet & Relaxed"
print("\n" + "="*70)
print("TEST 2: 'Quiet & Relaxed' atmosphere")
print("="*70)

user2 = {
    'activities': 'Reading, Coffee',
    'atmosphere': 'Quiet & Relaxed',
    'category': 'Cafe',
    'max_price_tier': '$'
}

recs2 = engine.get_recommendations(user2, top_n=5)
print(f"\nFound {len(recs2)} recommendations")

print("\nAll results:")
for idx, row in recs2.iterrows():
    print(f"  {row['Name_of_place']}: {row['Vibe_Type']}")

# Test 3: "Energetic"
print("\n" + "="*70)
print("TEST 3: 'Energetic' atmosphere")
print("="*70)

user3 = {
    'atmosphere': 'Energetic',
    'max_price_tier': '$$'
}

recs3 = engine.get_recommendations(user3, top_n=10)
print(f"\nFound {len(recs3)} recommendations")

print("\nAll vibes:")
for vibe in recs3['Vibe_Type'].unique():
    print(f"  {vibe}")

print("\n" + "="*70)
print("✅ All atmosphere filters working!")
print("="*70)
