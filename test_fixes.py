"""
Test the fixed recommendation engine.
"""
from recommendation_engine import NYCRecommendationEngine

print("Testing Fixed Recommendation Engine")
print("="*70)

engine = NYCRecommendationEngine()

# Test 1: Price filtering - should ONLY show $$ places
print("\n" + "="*70)
print("TEST 1: Price tier filtering (max_price_tier='$$')")
print("="*70)

user1 = {
    'activities': 'Eating',
    'atmosphere': 'Lively & Social',
    'max_price_tier': '$$'
}

recs1 = engine.get_recommendations(user1, top_n=10)
print(f"\nFound {len(recs1)} recommendations")
print("\nPrice tiers in results:")
print(recs1['price_tier'].value_counts())

print("\nTop 5:")
for idx, row in recs1.head().iterrows():
    print(f"  {row['Name_of_place']}: {row['price_tier']} - {row['Vibe_Type']}")

# Test 2: Atmosphere matching - should prefer Lively & Social vibes
print("\n" + "="*70)
print("TEST 2: Atmosphere matching ('Lively & Social')")
print("="*70)

user2 = {
    'activities': 'Dining, Entertainment',
    'atmosphere': 'Lively & Social',
    'max_price_tier': '$$'
}

recs2 = engine.get_recommendations(user2, top_n=10)
print(f"\nFound {len(recs2)} recommendations")

print("\nTop 5 with vibes:")
for idx, row in recs2.head().iterrows():
    print(f"  {row['Name_of_place']}")
    print(f"    Vibe: {row['Vibe_Type']}")
    print(f"    Price: {row['price_tier']}")
    print(f"    Match: {row['similarity_score']:.1%}")

# Test 3: Quiet atmosphere
print("\n" + "="*70)
print("TEST 3: Quiet atmosphere matching")
print("="*70)

user3 = {
    'activities': 'Reading, Working',
    'atmosphere': 'Quiet & Relaxed',
    'category': 'Cafe',
    'max_price_tier': '$'
}

recs3 = engine.get_recommendations(user3, top_n=5)
print(f"\nFound {len(recs3)} recommendations")

print("\nTop 5 with vibes:")
for idx, row in recs3.iterrows():
    print(f"  {row['Name_of_place']}")
    print(f"    Vibe: {row['Vibe_Type']}")
    print(f"    Price: {row['price_tier']}")
    print(f"    Match: {row['similarity_score']:.1%}")

print("\n" + "="*70)
print("Tests complete!")
print("="*70)
