from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

from data_app.main.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()