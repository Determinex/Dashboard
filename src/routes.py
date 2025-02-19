# src/routes.py

from apiflask import APIBlueprint
from flask import render_template, jsonify, request
import logging

# Create a blueprint for routes
bp = APIBlueprint('routes', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Route for the interactive directory tree explorer
@bp.route('/')
def directory_explorer():
    return render_template('directory_explorer.html')  # Serve the interactive tree explorer

# Route for the introductory page
@bp.route('/index.html')
def index():
    return render_template('index.html')  # Serve the introductory page

# Route for the homepage
@bp.route('/home')
def home():
    return render_template('homepage.html')  # Serve the homepage

# Route for bookmarks manager
@bp.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks_manager.html')  # Serve the bookmarks manager interface

# API route for handling bookmarks
@bp.route('/api/bookmarks', methods=['GET', 'POST'])
def handle_bookmarks():
    bookmark_manager = BookmarkManager()
    if request.method == 'GET':
        bookmarks = bookmark_manager.get_all_bookmarks()
        return jsonify(bookmarks)
    elif request.method == 'POST':
        data = request.json
        bookmark_manager.add_bookmark(data['title'], data['url'])
        return jsonify({"status": "success"}), 201