from bcrypt import checkpw
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get(username)
        if user and user.check_password(password):
            flash("Logged in successfully!", category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        flash("Username and password do not match", category='error')
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the user already exists
        user = User.get(username)
        if user:
            flash("Username already exists", category='error')

        # Check if the information is valid
        elif len(username) < 2:
            flash("Username must be greater than 1 character", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category='error')
        elif len(password1) < 5:
            flash("Password must be at least 5 characters", category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')

        # Create the user
        else:
            User.create(username, email, password1)
            user = User.get(username)
            print(user)
            flash("Account created!", category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("register.html")
