"""
Test the upscale atmosphere bug - getting casual results when selecting upscale.
"""
from recommendation_engine import NYCRecommendationEngine

print("Testing UPSCALE Atmosphere Bug")
print("="*70)

engine = NYCRecommendationEngine()

# Reproduce the bug: Select "Upscale" but get casual results
user_data = {
    'atmosphere': 'Upscale',
    'max_price_tier': '$$$$'
}

print("\nUser selected: Upscale atmosphere")
print("="*70)

recs = engine.get_recommendations(user_data, top_n=15)
print(f"\nFound {len(recs)} recommendations")

print("\nAll Vibe Types in results:")
print(recs['Vibe_Type'].value_counts())

print("\n\nDetailed Results:")
print("-"*70)
for idx, row in recs.iterrows():
    vibe = row['Vibe_Type']
    has_casual = 'casual' in str(vibe).lower() if vibe else False
    has_upscale = 'upscale' in str(vibe).lower() if vibe else False

    marker = ""
    if has_casual and not has_upscale:
        marker = "❌ BUG - Pure Casual!"
    elif has_casual and has_upscale:
        marker = "⚠️  Mixed (has both)"
    elif has_upscale:
        marker = "✅ Correct"
    else:
        marker = "❓ Other"

    print(f"{marker:25} {row['Name_of_place']:40} | Vibe: {vibe}")

print("\n" + "="*70)
print("ANALYSIS:")
print("="*70)
casual_only = recs[recs['Vibe_Type'].str.contains('asual', case=False, na=False) &
                   ~recs['Vibe_Type'].str.contains('pscale', case=False, na=False)]
print(f"Pure Casual results (BUG): {len(casual_only)}")
print(f"These should NOT appear when user selects 'Upscale'!")

if len(casual_only) > 0:
    print("\n❌ BUG CONFIRMED - Casual places showing up for Upscale preference")
else:
    print("\n✅ No bug - filtering working correctly")
