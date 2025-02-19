from flask import Flask
from src.config.config import Config
from src.routes import main as main_routes
from src.models import bookmark
import os

def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    app.config.from_object(config_class)
    
    # Initialize the database
    bookmark.init_app(app)
    
    # Register routes
    app.register_blueprint(main_routes.bp)
    
    # Setup other initializations here
    
    return app