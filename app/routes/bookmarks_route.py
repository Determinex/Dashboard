from flask import Blueprint, render_template
from flask_login import login_required

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/bookmarks_manager')
@login_required
def bookmarks_manager():
    return render_template('bookmarks_manager.html')