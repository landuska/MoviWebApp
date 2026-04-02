from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates

db = SQLAlchemy()

class User(db.Model):
    """
    Represents an user in the database.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): The unique name of the user. Cannot be empty.
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)


    @validates('name')
    def validate_name(self, key, value):
        """Validates that the user's name is not empty."""
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    def __repr__(self):
        return f"User (id={self.id}, name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Movie(db.Model):
    """
    Represents a movie in the database.

    Attributes:
        id (int): Primary key, auto-incremented.
        title (str): The unique title of the movie. Cannot be empty.
        release_year (int): The release year of the movie. Cannot be in the future.
        cover_url (str, optional): URL to the movie's cover image.
        user_id (int): Foreign key referencing the user.
        rating (int): Rating of the movie. Cannot be in the future.
    """
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    director: Mapped[str] = mapped_column(String, nullable=True)
    release_year: Mapped[int] = mapped_column(Integer)
    cover_url: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    rating: Mapped[int] = mapped_column(Float, nullable=True)

    @validates('title')
    def validate_title(self, key, value):
        """Validates that the movie's title is not empty."""
        if not value:
            raise ValueError("Title of movie cannot be empty")
        return value


    @validates('release_year')
    def validate_release_year(self, key, value):
        """
        Validates and cleans the release year.

        Converts string input to integer and ensures the year is not in the
        future.
        """
        if value is None:
            return None

        try:
            int_value = int(value)
        except ValueError:
            raise ValueError(f"Release year must be a valid number 'YYYY'")

        if int_value > date.today().year:
            raise ValueError("Release year cannot be in the future")
        return int_value


    @validates('cover_url')
    def validate_cover_url(self, key, value):
        """Validates that the cover URL is not empty and starts with valid web protocols."""
        if not value:
            return None

        if not ((value.startswith('http://') or value.startswith('https://'))):
            raise ValueError("URL of cover url should start with http:// or https://")
        return value if value else None

    @validates('rating')
    def validate_rating(self, key, value):
        """Validates that the rating is not more than 10."""
        if value is None:
            return None

        try:
            float_value = float(value)
        except ValueError:
            raise ValueError("Invalid rating. Must be a number.")

        if not (1 <= float_value <= 10):
            raise ValueError("Rating of movie should be from 1 to 10")

        return float_value


    def __repr__(self):
        return (f"Movie (id={self.id}, title={self.title}, director={self.director},"
                f" release_year={self.release_year}, cover_url={self.cover_url}, "
                f"user_id={self.user_id}, rating={self.rating})")

    def __str__(self):
        return f"{self.title} ({self.release_year})"