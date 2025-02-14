# src/models/folder.py
from . import db

class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)  # Self-referential foreign key

    parent = db.relationship('Folder', remote_side=[id], backref='subfolders')  # Relationship to allow parent-child access

    def __repr__(self):
        return f'<Folder {self.name}>'

    def get_ancestors(self):
        ancestors = []
        current_folder = self.parent
        while current_folder:
            ancestors.append(current_folder)
            current_folder = current_folder.parent
        return ancestors

    def get_descendants(self):
        descendants = []
        for subfolder in self.subfolders:
            descendants.append(subfolder)
            descendants.extend(subfolder.get_descendants())  # Recursively add subfolder descendants
        return descendants