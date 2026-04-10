from flask import Flask, render_template, request, redirect, Response, url_for, flash
from data_manager import DataManager
from models import User, Movie, db
from helpers import get_movie_with_api, get_and_validate_user, get_and_validate_movie
import os
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_file_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'data/movies.sqlite')}"
app.secret_key = 'flashkey'

db.init_app(app)

with app.app_context():
    db.create_all()

data_manager = DataManager()


@app.route('/', methods=['GET'])
def index()-> str:
    """
    Renders the home page with a list of all registered users.

    Returns:
        Rendered HTML template 'index.html' with users data.
    """
    users = data_manager.get_users()
    return render_template("index.html", users=users)

@app.route('/users', methods=['POST'])
def add_user()-> Response:
    """
    Creates a new user via a POST form.

    Redirects back to the index page after execution.
    """
    username = request.form.get('username', '').strip()
    try:
        data_manager.create_user(name=username)
        flash(f"User '{username}' was created successfully")

    except ValueError as e:
        flash(str(e))

    except SQLAlchemyError as e:
        flash(f"Database error: {str(e)}")

    except Exception:
        flash("Some error occurred. Please try again.")

    return redirect(url_for('index'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id: int) -> str | Response:
    """
    Fetches and displays the list of favorite movies for a specific user.

    Args:
        user_id (int): The ID of the user whose movies to retrieve.

    Returns:
        Rendered HTML template 'user_movies.html' with user and movie data.
    """
    input_user = get_and_validate_user(user_id, data_manager)
    if not input_user:
        return redirect(url_for('index'))

    movies = data_manager.get_movies(user_id=user_id)

    return render_template("user_movies.html", user=input_user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id: int)-> Response:
    """
    Fetches movie data from OMDb API and adds it to the user's list.

    Args:
        user_id (int): The ID of the user adding the movie.

    Returns:
        Redirects to the user's movie list page.
    """
    input_user = get_and_validate_user(user_id, data_manager)
    if not input_user:
        return redirect(url_for('index'))

    title = request.form.get('title')

    try:
        api_movie = get_movie_with_api(title)
        if not api_movie:
            flash(f"Movie '{title}' is not found in OMDb.")
            return redirect(url_for('get_movies', user_id=user_id))

        api_title, api_director, api_year, api_image, api_rating = api_movie

        new_movie = Movie(
            title=api_title,
            director=api_director,
            release_year=api_year,
            cover_url=api_image,
            user_id=user_id,
            rating=api_rating
        )

        data_manager.add_movie(movie=new_movie)
        flash(f"Movie '{api_title}' was created successfully")

    except ValueError as e:
        flash(str(e))

    except SQLAlchemyError as e:
        flash(f"Database error: {str(e)}")

    except Exception:
        flash("Some error occurred. Please try again.")

    return redirect(url_for('get_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id: int, movie_id: int)-> Response:
    """
    Updates the title of a specific movie in the user's list.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be updated.

    Returns:
        Redirects to the user's movie list page.
    """
    input_user = get_and_validate_user(user_id, data_manager)
    if not input_user:
        return redirect(url_for('index'))

    input_movie = get_and_validate_movie(user_id, movie_id, data_manager)

    if not input_movie:
        return redirect(url_for('get_movies',user_id=user_id))

    new_title = request.form.get('title')

    if not new_title:
        flash("Title cannot be empty.")
        return redirect(url_for('get_movies', user_id=user_id))

    try:
        data_manager.update_movie(movie_id, new_title)
        flash(f"Movie '{input_movie.title}' was updated successfully")

    except ValueError as e:
        flash(str(e))

    except SQLAlchemyError as e:
        flash(f"Database error: {str(e)}")

    except Exception:
        flash("Some error occurred. Please try again.")

    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id: int, movie_id: int)-> Response:
    """
    Removes a movie from the user's list of favorites.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be deleted.

    Returns:
        Redirects to the user's movie list page.
    """
    input_user = get_and_validate_user(user_id, data_manager)

    if not input_user:
        return redirect(url_for('index'))

    input_movie = get_and_validate_movie(user_id, movie_id, data_manager)

    if not input_movie:
        return redirect(url_for('get_movies', user_id=user_id))


    try:
        data_manager.delete_movie(movie_id)
        flash(f"Movie '{input_movie.title}' was deleted successfully")
    except ValueError as e:
        flash(str(e))

    except SQLAlchemyError as e:
        flash(f"Database error: {str(e)}")

    except Exception:
        flash("Some error occurred. Please try again.")

    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/delete', methods=['POST'])
def delete_user(user_id: int)-> Response:
    """
    Removes a user from the Database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Redirects to the main page.
    """
    input_user = get_and_validate_user(user_id, data_manager)

    if not input_user:
        return redirect(url_for('index'))

    try:
        data_manager.delete_user(user_id)
        flash(f"User '{input_user.name}' was deleted successfully")
    except ValueError as e:
        flash(str(e))

    except SQLAlchemyError as e:
        flash(f"Database error: {str(e)}")

    except Exception:
        flash("Some error occurred. Please try again.")

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """Handles HTTP 404 errors and displays a custom error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internet_server_error(e):
    """Handles HTTP 500 errors and displays a custom error page."""
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
