from sqlalchemy.exc import IntegrityError

from models import User, Movie, db


class DataManager():
    """
    Data manager for handling CRUD operations in the database.

    Encapsulates all direct database CRUD queries via SQLAlchemy
    for the User and Movie models.
    """
    def create_user(self, name: str)-> None:
        """
        Adds a new user to the database.

        Args:
            name (str): The unique name of the user.

        Raises:
            Exception: If the name fails validation or already exists in the database.
        """
        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            raise ValueError(f"User with name '{name}' already exists.")

        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def get_users(self) -> list[User]:
        """
        Get a list of all users from the database.

        Returns:
            list[User]: A list of objects for all registered users.
        """
        return db.session.query(User).all()

    def get_movies(self, user_id: int) -> list[Movie]:
        """
        Get a list of all movies added by a specific user.

        Args:
            user_id (int): The unique identifier (id) of the user whose
                           movies need to be found.

        Returns:
            list[Movie]: A list of Movie objects belonging to the given user.
        """
        return db.session.query(Movie).filter_by(user_id=user_id).all()

    def add_movie(self, movie: Movie) -> None:
        """
        Adds a new movie to a user's favorites list.

        Args:
            movie (Movie): A fully formed Movie object containing title,
                           director, release_year, cover_url, and user_id.
        """
        try:
            db.session.add(movie)
            db.session.commit()
        except IntegrityError:
            raise ValueError(f"Movie {movie} was already added to the user's favorites.")
        except Exception:
            db.session.rollback()
            raise

    def update_movie(self, movie_id: int, new_title: str) -> None:
        """
        Updates the title of an existing movie in the database.

        Args:
            movie_id (int): The unique identifier (id) of the movie to update.
            new_title (str): The new title for this movie.

        Raises:
            ValueError: If a movie with the specified movie_id is not found
                        in the database.
        """
        movie = db.session.get(Movie, movie_id)
        if movie:
            try:
                movie.title = new_title
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        else:
            raise ValueError(f"Movie with id {movie_id} not found")

    def delete_movie(self, movie_id: int) -> None:
        """
        Deletes a movie from the database (removes it from the user's favorites).

        Args:
            movie_id (int): The unique identifier (id) of the movie to delete.

        Raises:
            ValueError: If a movie with the specified movie_id is not found
                        in the database.
        """
        movie = db.session.get(Movie, movie_id)
        if movie:
            try:
                db.session.delete(movie)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        else:
            raise ValueError(f"Movie with id {movie_id} not found")



    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user from the database.

        Args:
            user_id (int): The unique identifier (id) of the user to delete.

        Raises:
            ValueError: If a usere with the specified user_id is not found
                        in the database.
        """
        user = db.session.get(User, user_id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        else:
            raise ValueError(f"User not found")