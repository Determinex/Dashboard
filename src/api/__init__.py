# api/__init__.py

from api_flask import APIFlask
from .routes import register_routes  # Import routes

app = APIFlask(__name__)

def create_app():
    register_routes(app)  # Register API routes
    return app