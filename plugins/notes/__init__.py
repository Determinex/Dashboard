from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from .models import Note
from app import db
import os

blueprint = Blueprint(
    'notes',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/notes/static'
)

@blueprint.route('/notes')
@login_required
def notes():
    """Render the notes page."""
    return render_template('notes.html')

@blueprint.route('/api/notes', methods=['GET', 'POST'])
@login_required
@cross_origin()
def api_notes():
    """Handle API requests for notes."""
    if request.method == 'POST':
        data = request.json
        new_note = Note(user_id=current_user.id, content=data['content'])
        db.session.add(new_note)
        db.session.commit()
        user_dir = os.path.join('user_data', current_user.uuid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        with open(os.path.join(user_dir, 'notes.txt'), 'a') as f:
            f.write(f"{new_note.content}\n")
        return jsonify({'message': 'Note added!'})
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([note.to_dict() for note in notes])

@blueprint.route('/api/notes/<int:id>', methods=['DELETE'])
@login_required
@cross_origin()
def delete_note(id):
    """Handle API requests to delete a note."""
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(note)
    db.session.commit()
    user_dir = os.path.join('user_data', current_user.uuid)
    notes_file = os.path.join(user_dir, 'notes.txt')
    if os.path.exists(notes_file):
        with open(notes_file, 'r') as f:
            lines = f.readlines()
        with open(notes_file, 'w') as f:
            for line in lines:
                if note.content not in line:
                    f.write(line)
    return jsonify({'message': 'Note deleted!'})

@blueprint.route('/api/notes/<int:id>', methods=['PUT'])
@login_required
@cross_origin()
def update_note(id):
    """Handle API requests to update a note."""
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    note.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Note updated!'})
