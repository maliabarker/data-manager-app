from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from data_app.models import User
from data_app.auth.forms import SignUpForm, LoginForm

# Import app and db from events_app package so that we can run app
from data_app.extensions import app, db, bcrypt

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
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