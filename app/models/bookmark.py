# filepath: /home/selph/Documents/Dashboard/src/models/bookmark.py
from . import db

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    folder = db.relationship('Folder', backref=db.backref('bookmarks', lazy=True))
    
def backup_database():
    import shutil
    shutil.copy('dashboard.db', 'backup/dashboard_backup.db')  # Backup database to the specified path