from flask import Blueprint, request, jsonify, url_for
from flask_login import login_user, logout_user, current_user
from src.models import User
from src import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    
    if user is None or not user.check_password(password):
        return jsonify(success=False, message='Invalid username or password')
    
    login_user(user)
    return jsonify(success=True, redirect_url=url_for('main.index'))

@auth_bp.route('/register', methods=['POST'])
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

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(success=True, redirect_url=url_for('main.index'))

@auth_bp.route('/auth_status', methods=['GET'])
def auth_status():
    return jsonify(is_authenticated=current_user.is_authenticated)
    