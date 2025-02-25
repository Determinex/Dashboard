# src/__init__.py

# ------------------------------------------------------------------------------ #
# File: src/__init__.py                                                          #
# Project: Dashboard                                                             #
# File Created: 2025-02-14 11:00:00                                              #
# Last Mod Date: 2025-02-24 16:00:00                                             #
# Last Mod By: Determinex                                                        #
# ------------------------------------------------------------------------------ #
# Component of: flask application source directory (src)                         #
# Used by: app.py                                                                #
# Description: This file contains the application setup                          #
# Content: Contains application's globally imported modules & setup functions    #
# ------------------------------------------------------------------------------ #

import os
import logging
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Verify environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
logging.info(f"Loaded SECRET_KEY: {SECRET_KEY}")
logging.info(f"Loaded DATABASE_URL: {DATABASE_URL}")

# Create the main APIFlask application
def create_app(config_class=None):
    app = APIFlask(__name__)

    # Load the configuration
    app.config.from_object(config_class or 'src.config.Config')

    # Initialize CORS
    from flask_cors import CORS
    CORS(app)

    # Initialize the database
    db.init_app(app)

    # Load the user object from the database
    @login_manager.user_loader
    def load_user(user_id):
        from src.models import User  # Ensure the User model is imported
        return User.query.get(int(user_id))

    # Create the database tables if not exist
    with app.app_context():
        if not os.path.exists(os.path.dirname(DATABASE_URL)):
            os.makedirs(os.path.dirname(DATABASE_URL))
            logging.info(f"Created database directory at {os.path.dirname(DATABASE_URL)}")
        db.create_all()
        logging.info("Database tables created")

    # Add CLI command for wiping the database
    @app.cli.command("wipe-db")
    def wipe_db():
        """Wipe the database by dropping all tables and recreating them."""
        with app.app_context():
            db.drop_all()
            db.create_all()
            logging.info("Database wiped and recreated successfully.")

    return app