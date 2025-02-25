# app.py
from apiflask import APIFlask
from flask_cors import CORS
from src import db, login_manager
from src.routes.main import bp as main_bp
from src.routes.auth import auth_bp
from src.routes.notes_route import notes_bp
from src.routes.bookmarks_route import bookmarks_bp
from src.routes.passwords_route import passwords_bp

def create_app(config_class=None):
    # Initialize the APIFlask app
    app = APIFlask(__name__)

    # Load the configuration
    app.config.from_object(config_class or 'src.config.Config')

    # Initialize CORS
    CORS(app)  # Enable CORS for all routes

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify login view for Flask-Login

    # Register blueprints for main app
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(passwords_bp)

    return app