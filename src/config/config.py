import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(DATABASE_DIR, "dashboard.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Additional configurations
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'production'
    DEBUG = os.environ.get('DEBUG') == 'True'
    TESTING = os.environ.get('TESTING') == 'False'
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

    # Debug prints
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"DATABASE_DIR: {DATABASE_DIR}")
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")
    print(f"ALLOWED_EXTENSIONS: {ALLOWED_EXTENSIONS}")
    print(f"MAX_CONTENT_LENGTH: {MAX_CONTENT_LENGTH}")
    print(f"FLASK_ENV: {FLASK_ENV}")
    print(f"DEBUG: {DEBUG}")
    print(f"TESTING: {TESTING}")
    print(f"LOG_LEVEL: {LOG_LEVEL}")

    # Ensure the database directory exists
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Ensure the logs directory exists
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR) 

    # Configure logging
    import logging
    logging.basicConfig(level=LOG_LEVEL)