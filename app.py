"""
Gradio interface for NYC Places Recommendation System.
Deployable to HuggingFace Spaces.
"""
import gradio as gr
import pandas as pd
from recommendation_engine import NYCRecommendationEngine

# Global variable for lazy loading
engine = None

def get_engine():
    """Lazy load the recommendation engine only when needed."""
    global engine
    if engine is None:
        print("Loading recommendation engine...")
        engine = NYCRecommendationEngine()
        print("Engine ready!")
    return engine

# Hardcoded categories to avoid loading engine at startup
AVAILABLE_CATEGORIES = [
    "Activity", "Bar", "Cafe", "Cocktail Lounge", "Entertainment",
    "Food", "Gallery", "Museum", "Night Life"
]


def get_recommendations(
    neighborhood,
    category,
    atmosphere,
    price_tier,
    activity_type,
    drinks,
    activities,
    music_genres,
    num_recommendations
):
    """
    Generate recommendations based on user inputs.
    All selections work as STRICT FILTERS - only places matching ALL criteria will be shown.
    """
    # Build user data with all filters
    user_data = {}

    # All of these are now strict filters
    if neighborhood and neighborhood != "Any":
        user_data['preferred_neighborhood'] = neighborhood

    if category and category != "Any":
        user_data['category'] = category

    if atmosphere and atmosphere != "Any":
        user_data['atmosphere'] = atmosphere

    if price_tier and price_tier != "Any":
        user_data['max_price_tier'] = price_tier

    if activity_type and activity_type != "Any":
        user_data['activity_type'] = activity_type

    if drinks:
        user_data['drinks'] = True

    # These are for semantic ranking (not strict filters)
    if activities:
        user_data['activities'] = activities

    if music_genres:
        user_data['music_genres'] = music_genres

    # Get recommendations (lazy load engine)
    try:
        eng = get_engine()
        recommendations = eng.get_recommendations(user_data, top_n=int(num_recommendations))

        if len(recommendations) == 0:
            return "No places found matching your criteria. Try relaxing some filters.", ""

        # Format results as a nice table
        results_df = recommendations[[
            'Name_of_place', 'Type', 'Category', 'Neighborhood',
            'price_tier', 'Vibe_Type', 'similarity_score'
        ]].copy()

        results_df.columns = ['Name', 'Type', 'Category', 'Neighborhood', 'Price', 'Vibe', 'Match Score']
        results_df['Match Score'] = results_df['Match Score'].apply(lambda x: f"{x:.1%}")

        # Create detailed view
        details = []
        for idx, row in recommendations.iterrows():
            details.append(f"""
### {row['Name_of_place']}
- **Type:** {row['Type']}
- **Category:** {row['Category']}
- **Neighborhood:** {row['Neighborhood']}
- **Address:** {row['Address']}
- **Vibe:** {row['Vibe_Type']}
- **Price:** {row['price_tier'] if pd.notna(row['price_tier']) else 'N/A'} ({row['Price_Level']})
- **Match Score:** {row['similarity_score']:.1%}

---
""")

        return results_df, "\n".join(details)

    except Exception as e:
        return f"Error: {str(e)}", ""


# Create Gradio interface
with gr.Blocks(title="NYC Places Recommendation System", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🗽 NYC Places Recommendation System

    Get personalized recommendations for places to visit in New York City based on your preferences!

    Powered by HuggingFace Transformers 🤖
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Filter Places")

            neighborhood = gr.Dropdown(
                choices=["Any", "Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island",
                        "SoHo", "West Village", "East Village", "Lower East Side",
                        "Upper West Side", "Upper East Side", "Midtown", "Williamsburg",
                        "Fort Greene", "Park Slope", "Brooklyn Heights", "Astoria"],
                label="Neighborhood",
                value="Any",
                info="Only show places in this neighborhood"
            )

            category = gr.Dropdown(
                choices=["Any"] + AVAILABLE_CATEGORIES,
                label="Category",
                value="Any",
                info="Only show places in this category"
            )

            atmosphere = gr.Dropdown(
                choices=["Any", "Lively & Social", "Quiet & Relaxed", "Casual",
                        "Upscale", "Energetic", "Artistic"],
                label="Atmosphere/Vibe",
                value="Any",
                info="Only show places with this vibe"
            )

            price_tier = gr.Radio(
                choices=["Any", "$", "$$", "$$$", "$$$$"],
                label="Maximum Price",
                value="Any",
                info="$ = Under $15, $$ = $15-40, $$$ = $41-80, $$$$ = Over $80"
            )

        with gr.Column():
            gr.Markdown("### Additional Filters")

            activity_type = gr.Radio(
                choices=["Any", "Solo", "Group", "Both"],
                label="Activity Type",
                value="Any",
                info="Solo = solo-friendly only, Group = group-friendly only"
            )

            drinks = gr.Checkbox(
                label="Must serve alcohol",
                value=False
            )

            activities = gr.Textbox(
                label="Activities (Optional)",
                placeholder="e.g., Eating, Museums, Art Galleries, Dancing",
                info="Used for ranking results"
            )

            music_genres = gr.Textbox(
                label="Music Preferences (Optional)",
                placeholder="e.g., Hip-Hop, Jazz, R&B, House",
                info="Used for ranking results"
            )

            num_recommendations = gr.Slider(
                minimum=1,
                maximum=20,
                value=5,
                step=1,
                label="Number of Results"
            )

            submit_btn = gr.Button("Get Recommendations", variant="primary", size="lg")

    gr.Markdown("### Your Recommendations")

    with gr.Row():
        results_table = gr.Dataframe(
            label="Quick View",
            wrap=True
        )

    with gr.Row():
        results_details = gr.Markdown(label="Detailed View")

    # Examples
    gr.Markdown("### Try These Examples")
    gr.Examples(
        examples=[
            ["Manhattan", "Food", "Lively & Social", "$$", "Both", True, "Eating, Fine Dining", "Hip-Hop, R&B", 5],
            ["Brooklyn", "Cafe", "Quiet & Relaxed", "$", "Solo", False, "Coffee, Reading, Working", "", 5],
            ["Upper East Side", "Any", "Upscale", "$$$", "Any", False, "Fine Dining", "", 5],
            ["Brooklyn", "Night Life", "Energetic", "$$", "Group", True, "Dancing, Music", "House, Hip-Hop", 5],
            ["Manhattan", "Museum", "Quiet & Relaxed", "$$", "Both", False, "Museums, Culture", "", 5],
        ],
        inputs=[neighborhood, category, atmosphere, price_tier, activity_type,
                drinks, activities, music_genres, num_recommendations],
    )

    # Connect button
    submit_btn.click(
        fn=get_recommendations,
        inputs=[neighborhood, category, atmosphere, price_tier, activity_type,
                drinks, activities, music_genres, num_recommendations],
        outputs=[results_table, results_details]
    )

    gr.Markdown("""
    ---
    ### About

    This recommendation system uses **strict filtering** combined with **AI-powered semantic ranking**.

    **How it works:**
    1. **Filter**: Only places matching ALL your selected criteria are shown
    2. **Rank**: Results are ranked using HuggingFace sentence-transformers based on your activity/music preferences

    **Example:** Selecting "Upper East Side" + "Upscale" will ONLY show upscale places in the Upper East Side.

    **Data:** 139 curated NYC locations
    **Tech Stack:** Python, HuggingFace Transformers, Gradio, Pandas, scikit-learn

    [GitHub Repository](https://github.com/ravencheneg/CapstoneProject)
    """)


if __name__ == "__main__":
    demo.launch()
