# app/models/__init__.py
# This file is used to import all the models

from .bookmark import Bookmark  
from .db import db
from .folder import Folder
from .note import Note, NoteContent
from .tag import Tag
from .user import User

# __all__ = ['db', 'User', 'Bookmark', 'Note', 'NoteContent', 'Folder', 'Tag']