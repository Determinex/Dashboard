# ------------------------------------------------------------------------------ #
# File: src/__init__.py                                                          #
# Project: Dashboard                                                             #
# File Created: 2025-02-14 11:00:00                                              #
# Last Mod Date: 2025-02-14 11:00:00                                             #
# Last Mod By: Determinex                                                        #
# ------------------------------------------------------------------------------ #
# Component of: flask application source directory (src)                         #
# Used by: app.py                                                                #
# Description: This file contains the application setup                          #
# Content: Contains application's globally imported modules & setup functions    #
# ------------------------------------------------------------------------------ #

import os # Import os
from flask import Flask # Import Flask
from flask_sqlalchemy import SQLAlchemy # Import SQLAlchemy
from flask_login import LoginManager # Import LoginManager
from flask_cors import CORS # Import CORS
from src.config import Config # Import Config
from src.models import db, User # Import User model
import logging # Import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'static')))
    
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)  # Enable CORS for all routes
    
    # Ensure the database directory exists
    if not os.path.exists(Config.DATABASE_DIR):
        os.makedirs(Config.DATABASE_DIR)
        logging.info(f"Created database directory at {Config.DATABASE_DIR}")
    
    # Initialize the database
    db.init_app(app)
    logging.info("Database initialized")
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    logging.info("Login manager initialized")
    
    # Register blueprints
    from src.routes.main import bp as main_bp
    from src.routes.auth import auth_bp
    from src.routes.notes_route import notes_bp
    from src.routes.bookmarks_route import bookmarks_bp
    from src.routes.passwords_route import passwords_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(passwords_bp)
    logging.info("Blueprints registered")
    
    # Create the database tables
    with app.app_context():
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
