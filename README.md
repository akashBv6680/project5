🎬 IMDB Movie Recommender
Welcome to the IMDB Movie Recommender! This is a web application that helps you discover new movies based on storyline similarity. The app scrapes movie data from IMDB and uses a text-based recommendation engine to suggest films you might enjoy.

✨ Features
Web Scraper: A Python script that uses Selenium to scrape movie titles and storylines from IMDb.

Recommendation Engine: A core script that preprocesses the data and uses cosine similarity to find the most similar movies to a user's input.

Interactive Web App: A user-friendly interface built with Streamlit where you can enter a storyline and get instant recommendations.

Data Storage: All movie data is stored in a .csv file for quick access.

🛠️ Installation
Clone the repository:

git clone https://github.com/akashBv6680/project5.git
cd project5

Create and activate a virtual environment:

Windows:

python -m venv venv
.\venv\Scripts\activate

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Install the required libraries:

pip install -r requirements.txt

🚀 How to Run the App
Follow these steps in order to get the app up and running.

1. Scrape Movie Data
First, run the scraper script to create the imdb_2024_movies.csv file.

python scraper.py

2. Run the Streamlit App
Once the data file is generated, you can start the web application.

streamlit run app.py

The app will open automatically in your browser. Happy recommending! 🍿
