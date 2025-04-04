from app import db

class Bookmark(db.Model):
    """Model for storing bookmarks."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)  # Optional description field
    tags = db.relationship(
        'Tag',
        secondary='bookmark_tag',
        back_populates='bookmarks',
        cascade="all, delete"  # Ensure cascade delete for associated tags
    )
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=True)
    directory = db.relationship('Directory', backref='bookmarks')  # Add this relationship

    def to_dict(self):
        """Convert the bookmark to a dictionary."""
        return {
            'id': self.id, # Ensure id is always included
            'url': self.url,  # Ensure url is always included
            'title': self.title, # Ensure title is always included
            'description': self.description,  # Ensure description is not None or Null
            'tags': [tag.name for tag in self.tags], # Convert tags to a list of names
            'directory': self.directory.name if self.directory else None # Include directory name if it exists
        }

class Tag(db.Model):
    """Model for storing tags."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    bookmarks = db.relationship('Bookmark', secondary='bookmark_tag', back_populates='tags')

class BookmarkTag(db.Model):
    """Model for the many-to-many relationship between bookmarks and tags."""
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

class Directory(db.Model):
    """Model for storing directories."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=True)
    parent = db.relationship('Directory', remote_side=[id], backref='children')

    def to_dict(self):
        """Convert the directory to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'parent': self.parent.name if self.parent else None
        }
