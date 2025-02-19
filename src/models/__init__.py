from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .bookmark import Bookmark
from .note import Note, NoteContent
from .folder import Folder
from .tag import Tag

__all__ = ['db', 'User', 'Bookmark', 'Note', 'NoteContent', 'Folder', 'Tag']