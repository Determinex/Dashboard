from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
import logging

bp = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Custom unauthorized handler to raise 401 error
@bp.app_errorhandler(401)
def unauthorized_callback(error):
    return render_template('errors/401.html'), 401

# Route for the home page
@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route to check authentication status
@bp.route('/auth_status', methods=['GET'])
def auth_status():
    return jsonify(is_authenticated=current_user.is_authenticated)

# Route for the dashboard page
@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Register error handlers
@bp.app_errorhandler(401)
@bp.app_errorhandler(403)
@bp.app_errorhandler(404)
@bp.app_errorhandler(405)
@bp.app_errorhandler(500)
def handle_errors(error):
    error_code = error.code
    error_pages = {
        401: 'errors/401.html',
        403: 'errors/403.html',
        404: 'errors/404.html',
        405: 'errors/405.html',
        500: 'errors/500.html'
    }
    error_page = error_pages.get(error_code, 'errors/generic_error.html')
    return render_template(error_page, error_message=str(error)), error_code