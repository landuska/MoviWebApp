from flask import Flask, render_template, request, redirect, url_for, flash
from models import User, Movie, db
import os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_file_path)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_root, 'data/library.sqlite')}"

db.init_app(app)

with app.app_context():
    db.create_all()