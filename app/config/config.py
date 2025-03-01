# app/config/config.py

import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(DATABASE_DIR, "dashboard.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Ensure the necessary directories exist
    for directory in [DATABASE_DIR, UPLOAD_FOLDER, os.path.join(BASE_DIR, 'logs')]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory at {directory}")

    @staticmethod
    def load_json_settings(filename):
        """Load JSON settings from a file."""
        with open(filename, 'r') as f:
            return json.load(f)