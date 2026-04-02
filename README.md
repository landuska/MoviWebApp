# 🎬 Flask Movie Manager

A web application built with **Flask** and **SQLAlchemy** to manage users and their favorite movies. The app integrates with the **OMDb API** to fetch movie details automatically.

---

## ✨ Features

### 👤 User Management
- Add users with unique names.
- Delete users and all their associated movies.

### 🎞️ Movie Management
- Add movies to a user’s favorite list by title.
- Fetch movie details from OMDb API (title, director, year, poster, IMDb rating).
- Update movie title.
- Delete movies from the list.

### 🛡️ Validation & Error Handling
- Data validated at the model level using SQLAlchemy `@validates`.
- Input checked in the controller with proper flash messages.
- Handles common errors (404, 500) with custom error pages.
- Defensive programming to prevent database corruption.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask  3.1.3
- **Database & ORM:** SQLite, SQLAlchemy  2.0.48
- **API:** OMDb API (via API key in `.env`)  

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.x installed on your machine.
- OMDb API key (create an account at [OMDb API](https://www.omdbapi.com/apikey.aspx)).

### 2. Installation & Setup

Clone the repository:

</>bash
```git clone https://github.com/landuska/MoviWebApp.git```

Install the required dependencies:

</>bash
```pip install flask flask-sqlalchemy requests SQLAlchemy Jinja2 python-dotenv```

Set up the .env file:
API_KEY=your_omdb_api_key

### 3. Running the Application
To start the local development server, run:

</>bash
```python app.py```

Open your web browser and go to http://localhost:5000. 
The SQLite database will be created automatically on the first run.

---

## 📂 Project Structure
```
book_alchemy/
├── app.py # Main Flask application with routes and error handlers
├── data_manager.py # Handles CRUD operations for User and Movie
├── models.py # SQLAlchemy models with validation
├── helpers.py # OMDb API integration and helper functions
├── config/ # Configuration folder
│ └── .env # Environment variables (e.g., OMDb API key)
├── data/ # Database storage
│ └── movies.sqlite # SQLite database (auto-created on first run)
├── templates/ # HTML templates for rendering pages
│ ├── base.html
│ ├── index.html
│ ├── user_movies.html
│ ├── 404.html
│ └── 500.html
└── static/ # Optional static files (CSS, JS, images)
```
---

# 🛡️ Architecture & Validation

## Model Level (`models.py`)
- Validates user names and movie fields (`title`, `release_year`, `cover_url`, `rating`)
- Ensures no empty fields, correct URLs, and ratings within 1–10

## Controller Level (`app.py`)
- Handles user input via forms
- Uses `try/except` and `flash` messages for error handling
- Prevents crashes and database corruption

## API Integration (`helpers.py`)
- Fetches movie details from OMDb using the API key
- Cleans invalid or missing data

---

## 📄 License
This project is an Education / Student Project and is open for learning and non-commercial use.
