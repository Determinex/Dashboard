from flask import Blueprint, render_template, jsonify
import logging

# Create a blueprint for routes
bp = Blueprint('routes', __name__)

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

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks_manager.html')  # Serve the bookmarks manager interface

@bp.route('/api/bookmarks', methods=['GET', 'POST'])
def handle_bookmarks():
    if request.method == 'GET':
        bookmarks = BookmarkManager().get_all_bookmarks()
        return jsonify(bookmarks)
    elif request.method == 'POST':
        data = request.json
        BookmarkManager().add_bookmark(data['title'], data['url'])
        return jsonify({"status": "success"}), 201

@app.route('/notes')
def notes():
    return render_template('notes_manager.html')  # Serve the notes manager interface

@app.route('/passwords')
def passwords():
    return render_template('password_manager.html')  # Serve the password manager interface