from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import User, Movie, db
from helpers import get_movie_with_api
import os

app = Flask(__name__)

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_file_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'data/movies.sqlite')}"
app.secret_key = 'flashkey'

db.init_app(app)

with app.app_context():
    db.create_all()

data_manager = DataManager()


@app.route('/', methods='GET')
def home():
    users = data_manager.get_users()
    return render_template("home.html", users=users)

@app.route('/users', methods=['POST'])
def add_user():
    username = request.form.get('username')

    if not username:
        flash("Username cannot be empty!")
        return redirect(url_for('home'))
    try:
        data_manager.create_user(name=username)
        flash(f"User '{username}' was created successfully")

    except ValueError as e:
        flash(f"Error: {str(e)}")

    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    users = data_manager.get_users()
    input_user = next((user for user in users if user.id == user_id), None)

    if not input_user:
        flash("User is not found.")
        return redirect(url_for('home'))

    movies = data_manager.get_movies(user_id=user_id)

    return render_template("user_movies.html", user=input_user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    users = data_manager.get_users()
    input_user = next((user for user in users if user.id == user_id), None)

    if not input_user:
        flash("User not found.")
        return redirect(url_for('home'))

    title = request.form.get('title')

    if not title:
        flash("Title cannot be empty")
        return redirect(url_for('get_movies', user_id=user_id))

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
        flash(f"Error: {str(e)}")

    return redirect(url_for('get_movies', user_id=user_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
