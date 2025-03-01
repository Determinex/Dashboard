# app/routes/__init__.py

from flask import Blueprint

# Import all your routes here
from .auth import auth_bp
from .bookmarks_route import bookmarks_bp
from .notes_route import notes_bp
from .passwords_route import passwords_bp
from .main import main_bp

# Create a list of all blueprints
blueprints = [auth_bp, bookmarks_bp, notes_bp, passwords_bp, main_bp]

def register_routes(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)