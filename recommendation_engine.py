# File: recommendation_engine.py
# Description: This module contains the core logic for the recommendation system,
#              including NLP preprocessing, TF-IDF, and Cosine Similarity.

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

# --- Download NLTK data (if not already downloaded) ---
# This is a one-time download needed for stopwords.
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')

# --- Global Variables ---
DATA_FILE = "imdb_2024_movies.csv"
RECOMMENDATION_COUNT = 5
movies_df = None
tfidf_vectorizer = None
tfidf_matrix = None

# --- Data Loading and Preprocessing ---
def load_and_preprocess_data():
    """
    Loads movie data from a CSV, cleans the storylines, and creates the TF-IDF matrix.
    """
    global movies_df, tfidf_vectorizer, tfidf_matrix
    
    try:
        movies_df = pd.read_csv(DATA_FILE)
        
        # Drop rows with missing values in the 'Storyline' column.
        movies_df.dropna(subset=['Storyline'], inplace=True)
        
        print("Data loaded and preprocessed.")
        print(f"Number of movies to analyze: {len(movies_df)}")
        
        # --- Text Cleaning ---
        # A simple function to clean the text.
        def clean_text(text):
            # Convert to lowercase.
            text = text.lower()
            # Remove special characters and punctuation.
            text = re.sub(r'[^a-z0-9\s]', '', text)
            # Remove stopwords.
            text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
            return text
            
        # Apply the cleaning function to the 'Storyline' column.
        movies_df['Cleaned Storyline'] = movies_df['Storyline'].apply(clean_text)
        
        # --- TF-IDF Vectorization ---
        # Create a TF-IDF Vectorizer instance.
        # This converts text documents into a matrix of TF-IDF features.
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
        # Fit and transform the cleaned storylines to create the TF-IDF matrix.
        tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['Cleaned Storyline'])
        
        print("TF-IDF matrix created.")
        
    except FileNotFoundError:
        print(f"Error: The file '{DATA_FILE}' was not found.")
        print("Please run scraper.py first to generate the dataset.")
        return False
    except Exception as e:
        print(f"An error occurred during data loading and preprocessing: {e}")
        return False
        
    return True

# --- Recommendation Logic ---
def get_recommendations(user_storyline):
    """
    Takes a user's storyline, finds the most similar movies, and returns the top 5.
    """
    if movies_df is None or tfidf_vectorizer is None or tfidf_matrix is None:
        print("Recommendation engine is not initialized. Please call load_and_preprocess_data() first.")
        return []

    # --- Preprocess User Input ---
    # The user's storyline must be preprocessed in the same way as the movie storylines.
    user_storyline = user_storyline.lower()
    user_storyline = re.sub(r'[^a-z0-9\s]', '', user_storyline)
    user_storyline = ' '.join([word for word in user_storyline.split() if word not in stopwords.words('english')])
    
    # --- Vectorize User Input ---
    # Convert the user's storyline into a TF-IDF vector.
    user_vector = tfidf_vectorizer.transform([user_storyline])

    # --- Calculate Cosine Similarity ---
    # Calculate the similarity between the user's input vector and all movie vectors.
    cosine_sim = cosine_similarity(user_vector, tfidf_matrix)

    # --- Get Top Recommendations ---
    # Get the indices of the movies with the highest similarity scores.
    # The `argsort()` function returns the indices that would sort the array.
    # We take the last few indices to get the highest scores.
    similarity_scores = list(enumerate(cosine_sim[0]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Select the top N movies (excluding the user's input movie if it were in the dataset).
    top_indices = [i[0] for i in similarity_scores[0:RECOMMENDATION_COUNT]]
    
    # Return the details of the recommended movies.
    recommended_movies = movies_df.iloc[top_indices][['Movie Name', 'Storyline']].to_dict('records')
    
    return recommended_movies

# --- Test the module (optional) ---
if __name__ == "__main__":
    if load_and_preprocess_data():
        sample_storyline = "A young wizard begins his journey at a magical school where he makes friends and enemies, facing dark forces along the way."
        recommendations = get_recommendations(sample_storyline)
        
        print("\n--- Sample Recommendations ---")
        if recommendations:
            for i, movie in enumerate(recommendations):
                print(f"{i+1}. Movie Name: {movie['Movie Name']}")
                print(f"   Storyline: {movie['Storyline']}\n")
        else:
            print("No recommendations found.")

