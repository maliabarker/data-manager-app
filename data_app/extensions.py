from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from data_app.models import User

import os

app = Flask(__name__)
app.config.from_object(Config)

db=SQLAlchemy(app)

# Authentication

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)