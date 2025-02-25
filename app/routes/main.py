from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
import logging

bp = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Route for the home page
@bp.route('/', methods=['GET'])
def index():
    logging.info("Home page accessed")
    return render_template('index.html')

# Route to check authentication status
@bp.route('/auth_status', methods=['GET'])
def auth_status():
    logging.info("Authentication status checked")
    return jsonify(is_authenticated=current_user.is_authenticated)

# Route for the dashboard page
@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    logging.info(f"Dashboard accessed by user: {current_user.username}")
    return render_template('dashboard.html')

# Custom error handler for unauthorized access
@bp.app_errorhandler(401)
def unauthorized_callback(error):
    logging.warning("Unauthorized access attempt")
    return render_template('errors/401.html'), 401