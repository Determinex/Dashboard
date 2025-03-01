from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Note, NoteContent

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes_manager')
@login_required
def notes_manager():
    notes = Note.query.all()
    return render_template('notes_manager.html', notes=notes)

@notes_bp.route('/save_note', methods=['POST'])
@login_required
def save_note():
    title = request.form['title']
    content = request.form['content']
    tag = request.form['tag']
    
    note_content = NoteContent(content=content)
    db.session.add(note_content)
    db.session.commit()
    
    new_note = Note(title=title, content_id=note_content.id, tag=tag)
    db.session.add(new_note)
    db.session.commit()
    
    flash('Note saved successfully!')
    return redirect(url_for('notes.notes_manager'))

@notes_bp.route('/blogspot')
@login_required
def blogspot():
    return render_template('blogspot.html')