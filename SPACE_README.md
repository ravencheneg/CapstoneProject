---
title: NYC Places Recommendation System
emoji: 🗽
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: gradio_app.py
pinned: false
license: mit
---

# NYC Places Recommendation System 🗽

An AI-powered recommendation engine that suggests personalized NYC places to visit based on your interests, preferences, and demographics.

## Features

- 🤖 **AI-Powered Matching**: Uses HuggingFace sentence-transformers for semantic similarity
- 🎯 **Personalized Recommendations**: Matches your unique preferences with 139+ NYC locations
- 💰 **Smart Filtering**: Filter by price tier ($-$$$$), category, solo/group friendly
- 📍 **All Boroughs**: Covers Manhattan, Brooklyn, Queens, Bronx, and Staten Island
- 🎨 **Interactive UI**: Easy-to-use Gradio interface

## How It Works

1. **Tell us your preferences**: What activities do you enjoy? What atmosphere do you prefer?
2. **Set your filters**: Budget, category, solo or group activities
3. **Get recommendations**: Receive personalized suggestions with match scores
4. **Explore NYC**: Discover new places tailored to your interests!

## Technology

- **HuggingFace Transformers**: `all-MiniLM-L6-v2` model for embeddings
- **Gradio**: Interactive web interface
- **Pandas & scikit-learn**: Data processing and similarity calculations
- **Python**: Backend logic

## Dataset

Contains 139 curated NYC locations across:
- 🍽️ Restaurants & Cafes
- 🎭 Entertainment Venues
- 🎨 Museums & Galleries
- 🌃 Nightlife Spots
- 🍸 Bars & Lounges

## Try It Out!

Use the examples or input your own preferences to discover amazing places in NYC!

---

Built with ❤️ using HuggingFace Transformers

[GitHub Repository](https://github.com/ravencheneg/CapstoneProject)
