# File: scraper.py
# Description: This script scrapes movie names and storylines from IMDB's 2024 movie list
#              and saves the data to a CSV file.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --- Setup Selenium WebDriver ---
# The webdriver_manager automatically handles the installation and management
# of the correct ChromeDriver, simplifying the setup process.
print("Setting up Selenium WebDriver...")
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print("WebDriver setup successful!")
except Exception as e:
    print(f"Error setting up WebDriver: {e}")
    print("Please ensure you have a compatible Chrome browser installed.")
    exit()

# --- Data to Scrape ---
# The target URL for 2024 movies on IMDB.
IMDB_URL = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"

# --- Main Scraping Function ---
def scrape_imdb():
    """
    Navigates to the IMDB URL, scrapes movie data, and returns it as a list of dictionaries.
    """
    print(f"Navigating to {IMDB_URL}...")
    driver.get(IMDB_URL)
    
    # Give the page some time to load all dynamic content.
    time.sleep(5)
    
    movie_data = []
    
    # Find all the movie list items on the page.
    # The movies are typically contained within elements with a specific class name.
    movie_list_items = driver.find_elements(By.CSS_SELECTOR, '.ipc-metadata-list-summary-item')
    
    # Iterate through each movie item to extract the details.
    if not movie_list_items:
        print("No movie items found. Please check the CSS selector or the URL.")
    
    for item in movie_list_items:
        try:
            # Scrape the movie name.
            movie_name_element = item.find_element(By.CSS_SELECTOR, '.ipc-title__text')
            movie_name = movie_name_element.text.split(' ', 1)[1].strip() if movie_name_element.text else "N/A"
            
            # Scrape the storyline/plot summary.
            storyline_element = item.find_element(By.CSS_SELECTOR, '.ipc-html-content-inner-div')
            storyline = storyline_element.text.strip() if storyline_element.text else "N/A"
            
            # Store the data as a dictionary.
            movie_data.append({
                "Movie Name": movie_name,
                "Storyline": storyline
            })
            print(f"Scraped: {movie_name}")
            
        except Exception as e:
            # Handle cases where some elements might be missing for a specific movie.
            print(f"Skipping a movie due to an error: {e}")
            continue
            
    print(f"Scraping complete. Found {len(movie_data)} movies.")
    return movie_data

# --- Execution ---
if __name__ == "__main__":
    scraped_movies = scrape_imdb()
    driver.quit()  # Close the browser instance.
    
    # Create a Pandas DataFrame from the scraped data.
    df = pd.DataFrame(scraped_movies)
    
    # Save the DataFrame to a CSV file.
    CSV_FILE_PATH = "imdb_2024_movies.csv"
    df.to_csv(CSV_FILE_PATH, index=False)
    
    print(f"\nData successfully saved to {CSV_FILE_PATH}")
    print(df.head()) # Print the first 5 rows to verify the data.

