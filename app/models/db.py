# src/models/db.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

class Model(db.Model):
    __abstract__ = True  # This class will not be instantiated directly