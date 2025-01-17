# db.py
import sqlite3
import os
from logger import Logger

class BaseDatabaseManager:
    def __init__(self):
        self.logger = Logger()
        self.connection = None
        self.setup_database()

    def get_database_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bookmarks.db')

    def execute_query(self, query, params=()):
        try:
            self.connection = sqlite3.connect(self.get_database_path())
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except Exception as e:
            self.logger.log_error(f"Database operation failed: {e}")
        finally:
            self.close_connection()

    def close_connection(self):
        if self.connection:
            self.connection.close()

class FolderManager(BaseDatabaseManager):
    def setup_database(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

    def add_folder(self, name):
        return self.execute_query('INSERT INTO folders (name) VALUES (?)', (name,))

class BookmarkManager(BaseDatabaseManager):
    def setup_database(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                folder_id INTEGER,
                is_favorite INTEGER DEFAULT 0,
                FOREIGN KEY (folder_id) REFERENCES folders (id)
            )
        ''')

    def add_bookmark(self, title, url, folder_id=None):
        return self.execute_query('INSERT INTO bookmarks (title, url, folder_id) VALUES (?, ?, ?)', (title, url, folder_id))

    def get_all_bookmarks(self):
        cursor = self.execute_query('SELECT * FROM bookmarks')
        return cursor.fetchall() if cursor else []

    def toggle_favorite(self, bookmark_id):
        self.execute_query('UPDATE bookmarks SET is_favorite = NOT is_favorite WHERE id = ?', (bookmark_id,))

class TagManager(BaseDatabaseManager):
    def setup_database(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
    
    def add_tag(self, name):
        return self.execute_query('INSERT INTO tags (name) VALUES (?)', (name,))