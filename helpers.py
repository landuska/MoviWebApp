import requests
import os
from dotenv import load_dotenv
import re
from flask import flash
from typing import Any
from models import User, Movie

load_dotenv(dotenv_path="config/.env")
API_KEY = os.getenv('API_KEY')


def clean_na(value: Any) -> str | None:
    """
    Cleans string values from garbage and OMDb-specific missing data markers.

    Converts empty strings and "N/A" values into a None object.

    Args:
        value (Any): The value received from the API to be cleaned.

    Returns:
        str: The cleaned string if the data is valid.
        None: If the value is empty, equals "N/A", or is already None.
    """
    if value is None:
        return None

    str_value = str(value).strip()
    if str_value.upper() == "N/A" or str_value == "":
        return None

    return str_value

def get_movie_with_api(t: str) -> tuple[str | None, str | None, str | None, str | None, float | None] | None:
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
        return None

    data = response.json()

    if data["Response"] == "False":
        print(f"Movie '{t}' not found")
        return None

    title = clean_na(data.get("Title"))
    director = clean_na(data.get("Director"))
    response_year = clean_na(data.get("Year"))
    image = clean_na(data.get("Poster"))
    response_rating = clean_na(data.get("imdbRating"))

    if response_year:
        digits_year = re.sub(r"[^0-9]", "", response_year)
        year = digits_year[:4] if digits_year else None
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

def get_and_validate_user(user_id: int, data_manager: Any) -> User | None:
    """
    Fetches a user from the database by their ID.

    If the user is not found, it creates a Flask flash message with an error.

    Args:
        user_id (int): The unique identifier of the user.
        data_manager (DataManager): The data manager object to interact with the DB.

    Returns:
        User: The found user object.
        None: If a user with this ID is not registered.
    """
    users = data_manager.get_users()
    input_user = next((user for user in users if user.id == user_id), None)

    if not input_user:
        flash("User not found.")

    return input_user

def get_and_validate_movie(user_id: int, movie_id: int, data_manager: Any) -> Movie | None:
    """
    Fetches  movie in the favorite list of a specific user.

    If the movie is not found or does not belong to this user, it creates
    a Flask flash message.

    Args:
        user_id (int): The unique identifier of the user.
        movie_id (int): The unique identifier of the movie.
        data_manager (DataManager): The data manager object to interact with the DB.

    Returns:
        Movie: The found movie object.
        None: If the movie is not found in this user's movie list.
    """
    movies = data_manager.get_movies(user_id=user_id)
    input_movie = next((movie for movie in movies if movie.id == movie_id), None)

    if not input_movie:
        flash("Movie not found.")

    return input_movie