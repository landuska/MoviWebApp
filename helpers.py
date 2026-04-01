import requests
import os
from dotenv import load_dotenv
import re

load_dotenv(dotenv_path="config/.env")
API_KEY = os.getenv('API_KEY')


def clean_na(value):
    if value is None:
        return None

    str_value = str(value).strip()
    if str_value.upper() == "N/A" or str_value == "":
        return None

    return str_value

def get_movie_with_api(t: str) -> tuple:
    """
    Fetches movie details from the OMDb API based on a title.

    Args:
        t (str): The title of the movie to search for.

    Returns:
        tuple: A tuple containing (title, director, year, image rating) if found.
        list: An empty list if the movie is not found or a network error occurs.
    """

    url_api = "https://www.omdbapi.com"

    params = {
        "apikey": API_KEY,
        "t": t,
    }

    try:
        response = requests.get(url_api, params=params)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

    data = response.json()

    if data["Response"] == "False":
        print(f"Movie '{t}' not found")
        return []

    title = clean_na(data.get("Title"))
    director = clean_na(data.get("Director"))
    response_year = clean_na(data.get("Year"))
    image = clean_na(data.get("Poster"))
    response_rating = clean_na(data.get("imdbRating"))

    if response_year:
        digits = re.sub(r"[^0-9]", "", response_year)
        year = digits[:4] if digits else None
    else:
        year = None

    if response_rating:
        try:
            rating = float(response_rating)
        except ValueError:
            rating = None
    else:
        rating = None

    return title, director, year, image, rating

print(get_movie_with_api("lalaland"))