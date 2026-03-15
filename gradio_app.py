"""
Gradio interface for NYC Places Recommendation System.
Deployable to HuggingFace Spaces.
"""
import gradio as gr
import pandas as pd
from recommendation_engine import NYCRecommendationEngine

# Initialize the recommendation engine
print("Loading recommendation engine...")
engine = NYCRecommendationEngine()
print("Engine ready!")

# Get available categories from the dataset
available_categories = sorted(engine.places_df['Category'].dropna().unique().tolist())


def get_recommendations(
    neighborhood,
    activities,
    atmosphere,
    music_genres,
    activity_type,
    drinks,
    price_tier,
    category,
    solo_friendly,
    group_friendly,
    num_recommendations
):
    """
    Generate recommendations based on user inputs.
    """
    # Build user profile
    user_data = {}

    if neighborhood and neighborhood != "Any":
        user_data['preferred_neighborhood'] = neighborhood

    if activities:
        user_data['activities'] = activities

    if atmosphere and atmosphere != "Any":
        user_data['atmosphere'] = atmosphere

    if music_genres:
        user_data['music_genres'] = music_genres

    if activity_type and activity_type != "Any":
        user_data['activity_type'] = activity_type

    user_data['drinks'] = drinks

    # Apply filters
    if price_tier and price_tier != "Any":
        user_data['max_price_tier'] = price_tier

    if category and category != "Any":
        user_data['category'] = category

    if solo_friendly:
        user_data['solo_friendly'] = True

    if group_friendly:
        user_data['group_friendly'] = True

    # Get recommendations
    try:
        recommendations = engine.get_recommendations(user_data, top_n=int(num_recommendations))

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
            gr.Markdown("### Your Preferences")

            neighborhood = gr.Dropdown(
                choices=["Any", "Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island",
                        "SoHo", "West Village", "East Village", "Lower East Side",
                        "Upper West Side", "Upper East Side", "Midtown", "Williamsburg",
                        "Fort Greene", "Park Slope", "Brooklyn Heights", "Astoria"],
                label="Preferred Neighborhood",
                value="Any"
            )

            activities = gr.Textbox(
                label="Favorite Activities",
                placeholder="e.g., Eating, Museums, Art Galleries, Dancing",
                info="Separate multiple activities with commas"
            )

            atmosphere = gr.Dropdown(
                choices=["Any", "Lively & Social", "Quiet & Relaxed", "Casual",
                        "Upscale", "Energetic", "Artistic"],
                label="Preferred Atmosphere",
                value="Any"
            )

            music_genres = gr.Textbox(
                label="Music Preferences (Optional)",
                placeholder="e.g., Hip-Hop, Jazz, R&B, House",
                info="Separate multiple genres with commas"
            )

            activity_type = gr.Radio(
                choices=["Any", "Solo", "Group", "Both"],
                label="Activity Type",
                value="Any"
            )

            drinks = gr.Checkbox(
                label="Interested in places that serve alcohol",
                value=False
            )

        with gr.Column():
            gr.Markdown("### Filters")

            price_tier = gr.Radio(
                choices=["Any", "$", "$$", "$$$", "$$$$"],
                label="Maximum Price Tier",
                value="Any",
                info="$ = Under $15, $$ = $15-40, $$$ = $41-80, $$$$ = Over $80"
            )

            category = gr.Dropdown(
                choices=["Any"] + available_categories,
                label="Category",
                value="Any"
            )

            solo_friendly = gr.Checkbox(
                label="Solo Friendly Only",
                value=False
            )

            group_friendly = gr.Checkbox(
                label="Group Friendly Only",
                value=False
            )

            num_recommendations = gr.Slider(
                minimum=1,
                maximum=20,
                value=5,
                step=1,
                label="Number of Recommendations"
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
            ["Manhattan", "Eating, Fine Dining", "Lively & Social", "Hip-Hop, R&B", "Both", True, "$$", "Food", False, False, 5],
            ["Brooklyn", "Coffee, Reading, Working", "Quiet & Relaxed", "", "Solo", False, "$", "Cafe", True, False, 5],
            ["Manhattan", "Art, Galleries", "Quiet & Relaxed", "", "Solo", False, "$", "Gallery", True, False, 5],
            ["Brooklyn", "Dancing, Music", "Energetic", "House, Hip-Hop", "Group", True, "$$", "Night Life", False, True, 5],
            ["Manhattan", "Museums, Culture", "Quiet & Relaxed", "", "Both", False, "$$", "Museum", False, False, 5],
        ],
        inputs=[neighborhood, activities, atmosphere, music_genres, activity_type,
                drinks, price_tier, category, solo_friendly, group_friendly, num_recommendations],
    )

    # Connect button
    submit_btn.click(
        fn=get_recommendations,
        inputs=[neighborhood, activities, atmosphere, music_genres, activity_type,
                drinks, price_tier, category, solo_friendly, group_friendly, num_recommendations],
        outputs=[results_table, results_details]
    )

    gr.Markdown("""
    ---
    ### About

    This recommendation system uses **HuggingFace sentence-transformers** to match your preferences
    with 139 curated NYC locations. It analyzes semantic similarity between your preferences and
    place characteristics to provide personalized recommendations.

    **Tech Stack:** Python, HuggingFace Transformers, Gradio, Pandas, scikit-learn

    [GitHub Repository](https://github.com/ravencheneg/CapstoneProject)
    """)


if __name__ == "__main__":
    demo.launch()
