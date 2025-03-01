# dashboard/app/app.py

import os
import logging
from flask import Flask
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from app.models import Bookmark, Folder, Note, Tag, User, db
from app.routes import register_routes

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    api = APIFlask(__name__)  # Create an APIFlask instance

    # Load the configuration
    app.config.from_object(config_class or 'app.config.config.Config')

    # Enable Cross-Origin Resource Sharing
    CORS(app)
    
    # Initialize components
    init_extensions(app)
    register_blueprints(app)

    return app, api  # Return both Flask and APIFlask instances

def init_extensions(app):
    """Initialize extensions for the Flask application."""
    db.init_app(app)  # Initialize the database
    login_manager.init_app(app)  # Initialize the login manager
    login_manager.login_view = 'auth.login'  # Specify login view for Flask-Login

# Run the application
if __name__ == '__main__':
    app, api = create_app()  # Create instances of Flask and APIFlask
    app.run(debug=True)  # Start the Flask server in debug mode
