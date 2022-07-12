from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from data_app.models import User
from data_app.auth.forms import SignUpForm, LoginForm

# Import app and db from events_app package so that we can run app
from data_app.extensions import app, db, bcrypt

from data_app.util.helpers import upload_file_to_s3

auth = Blueprint("auth", __name__)

# for uploading files
ALLOWED_EXTENSIONS = {'png'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # check whether an input field with name 'user_file' exist
        if 'profile_picture' not in request.files:
            flash('No profile picture selected')
            return redirect(url_for('auth.signup'))

        # after confirm 'user_file' exist, get the file from input
        profile_pic = form.profile_picture.data
        print(profile_pic)

        # check whether a file is selected
        if profile_pic.filename == '':
            flash('No selected file')
            return redirect(url_for('auth.signup'))

        # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
        if profile_pic and allowed_file(profile_pic.filename):
            output = upload_file_to_s3(profile_pic, 'profile_pics')

            # if upload success,will return file name of uploaded file
            if output:
                # write your code here
                user = User(
                    username = form.username.data,
                    profile_picture = profile_pic.filename,
                    password = hashed_password
                )
                db.session.add(user)
                db.session.commit()
                flash('Account Successfully Created')
                return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        flash(f'Logged in as {current_user.username}')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash(f'Successfully logged out')
    return redirect(url_for('main.homepage'))