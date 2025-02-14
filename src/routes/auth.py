# src/routes/auth.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user
from src import db
from src.models import User
from src.auth.forms import LoginForm
from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()  # Form for login
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/register', methods=['POST'])
def register():
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
    
    login_user(new_user)
    return jsonify(success=True, redirect_url=url_for('main.index'))

@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(success=True, redirect_url=url_for('main.index'))

@bp.route('/auth_status', methods=['GET'])
def auth_status():
    return jsonify(is_authenticated=current_user.is_authenticated)
    