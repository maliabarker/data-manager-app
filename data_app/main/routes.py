from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user
from datetime import date, datetime
from data_app.models import User
# from data_app.main.forms import DonationPlaceForm, DonationItemForm
import os
from werkzeug.utils import secure_filename

from data_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

@main.route('/')
def homepage():
    return render_template('home.html', user=current_user)