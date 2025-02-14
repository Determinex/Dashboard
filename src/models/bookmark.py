# filepath: /home/selph/Documents/Dashboard/src/models/bookmark.py
from . import db

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=True)
    
    # Relationships
    folder = db.relationship('Folder', backref=db.backref('bookmarks', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('bookmarks', lazy=True))

    def __repr__(self):
        return f'<Bookmark {self.title}>'
    def __init__(self, title, url, folder_id=None, tag_id=None):
        self.title = title
        self.url = url
        self.folder_id = folder_id
        self.tag_id = tag_id
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'folder_id': self.folder_id,
            'tag_id': self.tag_id
        }
    @staticmethod
    def from_dict(data):
        return Bookmark(
            title=data['title'],
            url=data['url'],
            folder_id=data.get('folder_id'),
            tag_id=data.get('tag_id')
        )
    @staticmethod
    def from_dict_list(data_list):
        return [Bookmark.from_dict(data) for data in data_list]
    @staticmethod
    def to_dict_list(bookmarks):
        return [bookmark.to_dict() for bookmark in bookmarks]
    @staticmethod
    def get_bookmark_by_id(bookmark_id):
        return Bookmark.query.get(bookmark_id)
    @staticmethod
    def get_all_bookmarks():
        return Bookmark.query.all()
    @staticmethod
    def add_bookmark(bookmark):
        db.session.add(bookmark)
        db.session.commit()
    @staticmethod
    def update_bookmark(bookmark):
        db.session.commit()
    @staticmethod
    def delete_bookmark(bookmark):
        db.session.delete(bookmark)
        db.session.commit()
    @staticmethod
    def get_bookmarks_by_folder(folder_id):
        return Bookmark.query.filter_by(folder_id=folder_id).all()
    @staticmethod
    def get_bookmarks_by_tag(tag_id):
        return Bookmark.query.filter_by(tag_id=tag_id).all()
    @staticmethod
    def get_bookmarks_by_folder_and_tag(folder_id, tag_id):
        return Bookmark.query.filter_by(folder_id=folder_id, tag_id=tag_id).all()
    @staticmethod
    def get_bookmarks_by_folder_or_tag(folder_id, tag_id):
        return Bookmark.query.filter((Bookmark.folder_id == folder_id) | (Bookmark.tag_id == tag_id)).all()