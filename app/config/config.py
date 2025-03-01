# app/config/config.py

import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class DirectoryConfig:
    """Directory configuration class."""
    
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')

    @staticmethod
    def ensure_directories_exist():
        """Ensure that necessary directories exist."""
        for directory in [DirectoryConfig.DATABASE_DIR, DirectoryConfig.UPLOAD_FOLDER, DirectoryConfig.LOGS_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Created directory at {directory}")

class Config:
    """Base configuration class."""
    
    # Sensitive Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # This will be overridden in DevConfig
    API_KEY = os.getenv('API_KEY')

    # General Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Default values for non-sensitive variables
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Ensure the necessary directories exist
    DirectoryConfig.ensure_directories_exist()

    @staticmethod
    def load_json_settings(filename):
        """Load JSON settings from a file."""
        with open(filename, 'r') as f:
            return json.load(f)

class DevConfig(Config):
    """Development configuration class."""
    DEBUG = True  # Enable debug mode
    # Specify the local SQLite database URI directly
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DirectoryConfig.DATABASE_DIR, 'dashboard.db')
    LOG_LEVEL = 'DEBUG'  # Set log level to DEBUG for development

class ProdConfig(Config):
    """Production configuration class."""
    DEBUG = False  # Disable debug mode
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Use the environment variable for production
    LOG_LEVEL = 'ERROR'  # Set log level to ERROR for production