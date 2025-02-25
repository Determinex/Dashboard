# api/__init__.py

from apiflask import APIFlask # Import APIFlask
from .routes import register_routes  # Import routes

# Create an instance of APIFlask
api = APIFlask(__name__)

# Create the main APIFlask application
def create_app():
    register_routes(api)  # Register API routes
    return api  # Return the APIFlask application instance