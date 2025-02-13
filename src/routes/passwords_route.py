from flask import Blueprint, render_template
from flask_login import login_required

passwords_bp = Blueprint('passwords', __name__)

@passwords_bp.route('/passwords_manager')
@login_required
def passwords_manager():
    return render_template('passwords_manager.html')