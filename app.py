from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import User, Movie, db
from helpers import get_movie_with_api
import os

app = Flask(__name__)

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_file_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'data/library.sqlite')}"
app.secret_key = 'flashkey'

db.init_app(app)

with app.app_context():
    db.create_all()

data_manager = DataManager()



