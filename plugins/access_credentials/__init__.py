from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from .models import AccessCredential
from app import db
import os

blueprint = Blueprint(
    'access_credentials',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/access_credentials/static'
)

@blueprint.route('/access_credentials')
@login_required
def access_credentials():
    """Render the access credentials page."""
    return render_template('access_credentials.html')

@blueprint.route('/api/access_credentials', methods=['GET', 'POST'])
@login_required
@cross_origin()
def api_access_credentials():
    """Handle API requests for access credentials."""
    if request.method == 'POST':
        data = request.json
        new_credential = AccessCredential(user_id=current_user.id, service=data['service'], username=data['username'], password=data['password'])
        db.session.add(new_credential)
        db.session.commit()
        user_dir = os.path.join('user_data', current_user.uuid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        with open(os.path.join(user_dir, 'access_credentials.txt'), 'a') as f:
            f.write(f"{new_credential.service} - {new_credential.username} - {new_credential.password}\n")
        return jsonify({'message': 'Access credential added!'})
    credentials = AccessCredential.query.filter_by(user_id=current_user.id).all()
    return jsonify([credential.to_dict() for credential in credentials])

@blueprint.route('/api/access_credentials/<int:id>', methods=['DELETE'])
@login_required
@cross_origin()
def delete_access_credential(id):
    """Handle API requests to delete an access credential."""
    credential = AccessCredential.query.get_or_404(id)
    if credential.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(credential)
    db.session.commit()
    user_dir = os.path.join('user_data', current_user.uuid)
    credentials_file = os.path.join(user_dir, 'access_credentials.txt')
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            lines = f.readlines()
        with open(credentials_file, 'w') as f:
            for line in lines:
                if f"{credential.service} - {credential.username} - {credential.password}" not in line:
                    f.write(line)
    return jsonify({'message': 'Access credential deleted!'})

@blueprint.route('/api/access_credentials/<int:id>', methods=['PUT'])
@login_required
@cross_origin()
def update_access_credential(id):
    """Handle API requests to update an access credential."""
    credential = AccessCredential.query.get_or_404(id)
    if credential.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    credential.service = data['service']
    credential.username = data['username']
    credential.password = data['password']
    db.session.commit()
    return jsonify({'message': 'Access credential updated!'})
