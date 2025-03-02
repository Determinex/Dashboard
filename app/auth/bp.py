# app/auth/bp.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask import Blueprint
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm # Import both forms
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(success=True, redirect_url=url_for('main.index')) # Kept the jsonify response for consistency


@bp.route('/register_json', methods=['POST']) # Added a new JSON endpoint for registration
def register_json():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return jsonify(success=False, message='Passwords do not match')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(success=False, message='Username already exists')

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(success=True, message='User registered successfully')


@bp.route('/auth_status', methods=['GET'])
def auth_status():
    return jsonify(is_authenticated=current_user.is_authenticated)
