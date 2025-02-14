# src/models/db.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

class Model(db.Model):
    __abstract__ = True  # This class will not be instantiated directly

def backup_database():
    import shutil
    shutil.copy('dashboard.db', 'backup/dashboard_backup.db')  # Backup database to the specified path