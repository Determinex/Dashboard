# app/__init__.py

# ------------------------------------------------------------------------------ #
# File: app/__init__.py                                                          #
# Project: Dashboard                                                             #
# File Created: 2025-02-14 11:00:00                                              #
# Last Mod Date: 2025-02-25 18:00:00                                             #
# Last Mod By: Determinex                                                        #
# ------------------------------------------------------------------------------ #
# Component of: flask application source directory (app)                         #
# Used by: app.py                                                                #
# Description: This file contains the application setup                          #
# Content: Contains application's globally imported modules & setup functions    #
# ------------------------------------------------------------------------------ #

# app/__init__.py

import os
import logging
from flask import Flask
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    api = APIFlask(__name__)  # Create an APIFlask instance

    # Load the configuration
    app.config.from_object(config_class or 'app.config.Config')

    # Initialize components
    CORS(app)  # Enable Cross-Origin Resource Sharing
    init_extensions(app)
    register_blueprints(app)

    return app, api  # Return both Flask and APIFlask instances

def init_extensions(app):
    """Initialize extensions for the Flask application."""
    db.init_app(app)  # Initialize the database
    login_manager.init_app(app)  # Initialize the login manager
    login_manager.login_view = 'auth.login'  # Specify login view for Flask-Login

def register_blueprints(app):
    """Register blueprints for the Flask application."""
    from app.routes.main import bp as main_bp
    from app.routes.auth import auth_bp
    from app.routes.notes_route import notes_bp
    from app.routes.bookmarks_route import bookmarks_bp
    from app.routes.passwords_route import passwords_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(passwords_bp)

if __name__ == '__main__':
    # Create the Flask and APIFlask applications
    flask_app, api_app = create_app()

    # Start both applications on different threads/ports
    import threading

    def run_flask():
        flask_app.run(port=5000)

    def run_api():
        api_app.run(port=5001)

    flask_thread = threading.Thread(target=run_flask)
    api_thread = threading.Thread(target=run_api)

    flask_thread.start()
    api_thread.start()

    flask_thread.join()
    api_thread.join()
