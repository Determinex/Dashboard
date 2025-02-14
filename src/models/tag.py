# filepath: /home/selph/Documents/Dashboard/src/models/tag.py
from . import db
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)