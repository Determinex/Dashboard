# dashboard/app/__init__.py

import os
from flask import Flask
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from app.config import DevConfig, ProdConfig
from app.models import Bookmark, Folder, Note, Tag, User, db
from app.routes import register_routes

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    api = APIFlask(__name__)  # Create an APIFlask instance

    # Load the configuration
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    # Enable Cross-Origin Resource Sharing
    CORS(app)
    
    # Initialize components
    init_extensions(app)
    register_routes(app)  # Ensure this function is defined in your routes module

    return app, api  # Return both Flask and APIFlask instances

def init_extensions(app):
    """Initialize extensions for the Flask application."""
    db.init_app(app)  # Initialize the database
    login_manager.init_app(app)  # Initialize the login manager
    login_manager.login_view = 'auth.login'  # Specify login view for Flask-Login