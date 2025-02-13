import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from src.config import Config
from src.models import db, User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'static')))
    
    app.config.from_object(config_class)
    
    # Ensure the database directory exists
    if not os.path.exists(Config.DATABASE_DIR):
        os.makedirs(Config.DATABASE_DIR)
    
    # Initialize the database
    db.init_app(app)
    print("Database initialized")
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    print("Login manager initialized")
    
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
    print("Blueprints registered")
    
    # Create the database tables
    with app.app_context():
        db.create_all()
        print("Database tables created")
    
    # Add CLI command for wiping the database
    @app.cli.command("wipe-db")
    def wipe_db():
        """Wipe the database by dropping all tables and recreating them."""
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Database wiped and recreated successfully.")
    
    return app