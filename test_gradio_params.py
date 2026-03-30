"""
Test with exact parameters as they would come from Gradio interface.
"""
from recommendation_engine import NYCRecommendationEngine

print("Testing with GRADIO-style Parameters")
print("="*70)

engine = NYCRecommendationEngine()

# Simulate selecting "Upscale" from the dropdown in Gradio
# This is exactly how app.py builds the user_data dict

atmosphere = "Upscale"  # From Gradio dropdown
category = "Any"
price_tier = "Any"

user_data = {}

# This mimics the logic in app.py lines 43-44
if atmosphere and atmosphere != "Any":
    user_data['atmosphere'] = atmosphere

print(f"User selected atmosphere: '{atmosphere}'")
print(f"user_data dict: {user_data}")
print("="*70)

recs = engine.get_recommendations(user_data, top_n=15)
print(f"\nFound {len(recs)} recommendations")

print("\nAll Vibe Types in results:")
for vibe in recs['Vibe_Type'].unique():
    print(f"  - {vibe}")

print("\n\nDetailed Results:")
print("-"*70)
for idx, row in recs.iterrows():
    vibe = row['Vibe_Type']
    has_casual = 'casual' in str(vibe).lower() if vibe else False
    has_upscale = 'upscale' in str(vibe).lower() if vibe else False

    marker = ""
    if has_casual and not has_upscale:
        marker = "❌ BUG"
    elif has_casual and has_upscale:
        marker = "⚠️  Mixed"
    elif has_upscale:
        marker = "✅"
    else:
        marker = "❓"

    score = row['similarity_score']
    print(f"{marker:5} {row['Name_of_place']:35} | {vibe:30} | Score: {score:.3f}")

# Now test without any filters at all to see what ranks highest
print("\n\n" + "="*70)
print("TEST 2: NO atmosphere filter (just semantic matching)")
print("="*70)

user_data2 = {
    'activities': 'Fine Dining',
}

recs2 = engine.get_recommendations(user_data2, top_n=15)
print(f"\nFound {len(recs2)} recommendations")
print("\nTop 10 by similarity (NO atmosphere filter):")
for idx, row in recs2.head(10).iterrows():
    print(f"  {row['Name_of_place']:35} | {row['Vibe_Type']:30} | {row['similarity_score']:.3f}")
