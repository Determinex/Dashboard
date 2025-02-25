import os
from sqlalchemy import inspect, text
from src.models import db

def get_directory_info(directory):
    total_size = 0
    total_files = 0
    total_dirs = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        total_dirs += len(dirnames)
        total_files += len(filenames)
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return {
        'total_size': total_size,
        'total_files': total_files,
        'total_dirs': total_dirs
    }

def get_database_info():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    table_info = {}

    for table in tables:
        count = db.session.execute(text(f'SELECT COUNT(*) FROM {table}')).scalar()
        table_info[table] = count

    # Retrieve the database file path
    db_path = db.engine.url.database
    db_size = os.path.getsize(db_path)

    return {
        'db_size': db_size,
        'tables': table_info
    }