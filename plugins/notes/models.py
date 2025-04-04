from app import db

class Notebook(db.Model):
    """Model for storing notebooks."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sections = db.relationship('Section', backref='notebook', lazy=True)

    def to_dict(self):
        """Convert the notebook to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'sections': [section.to_dict() for section in self.sections]
        }

class Section(db.Model):
    """Model for storing notebook sections."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'), nullable=False)
    notes = db.relationship('Note', backref='section', lazy=True)

    def to_dict(self):
        """Convert the section to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'notes': [note.to_dict() for note in self.notes]
        }

class Note(db.Model):
    """Model for storing notes."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """Convert the note to a dictionary."""
        return {
            'id': self.id,
            'content': self.content,
            'section_id': self.section_id,
            'notebook_id': self.notebook_id
        }
