# File: app.py
# Description: This script creates an interactive Streamlit web application for
#              the IMDB movie recommendation system with a background image.

import streamlit as st
import base64
from recommendation_engine import load_and_preprocess_data, get_recommendations
import sys

# --- Helper function to convert an image to Base64 ---
def get_base64_image(image_path):
    """
    Reads an image from a file path and returns its Base64-encoded string.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return None

# --- Main Streamlit App Code ---
# Set up the custom CSS for the background image.
# We are now getting the image from the same directory as the script.
image_file_path = "imdb.jpg"
background_image_base64 = get_base64_image(image_file_path)

if background_image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{background_image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Could not find the background image 'imdb.jpg'. Please ensure it is in the same folder as this script.")

# --- Set Up the Streamlit Page ---
st.set_page_config(
    page_title="IMDB Movie Recommendations",
    page_icon="🎬",
    layout="wide"
)

# --- App Title and Description ---
st.title("🎬 IMDB Movie Recommender")
st.markdown("### Find movies based on storylines!")
st.write(
    "This app recommends movies from IMDB's 2024 list based on storyline similarity. "
    "Simply enter a short plot description and click 'Get Recommendations'."
)
st.markdown("---")

# --- Load the Recommendation Engine ---
# This part runs once when the app starts.
try:
    with st.spinner("Loading and preprocessing data... This may take a moment."):
        # Assuming recommendation_engine.py is in the same directory and works correctly
        engine_loaded = load_and_preprocess_data()
    
    if not engine_loaded:
        st.error("Could not load the recommendation engine. Please ensure 'imdb_2024_movies.csv' exists.")
        st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred during engine setup: {e}")
    st.stop()

# --- User Input ---
# Create a text area for the user to input their storyline.
user_storyline = st.text_area(
    "Enter a movie storyline or a short plot description:",
    placeholder="e.g., A young wizard begins his journey at a magical school where he makes friends and enemies, facing dark forces along the way."
)

# Create a button to trigger the recommendations.
if st.button("Get Recommendations"):
    if user_storyline:
        with st.spinner("Finding similar movies..."):
            try:
                # Get the recommendations from the engine.
                recommendations = get_recommendations(user_storyline)
            except Exception as e:
                st.error(f"An error occurred while getting recommendations: {e}")
                recommendations = []

        if recommendations:
            st.markdown("### Top 5 Recommended Movies")
            
            # Display each recommended movie in a structured way.
            for i, movie in enumerate(recommendations):
                st.markdown(
                    f"*{i+1}. {movie['Movie Name']}*"
                )
                st.write(f"*Storyline:* {movie['Storyline']}")
                st.markdown("---")
        else:
            st.warning("No recommendations found for this storyline. Try a different one.")
    else:
        st.warning("Please enter a storyline to get recommendations.")
