import sqlite3

# Function to create the database and tables
def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create bookmarks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT NOT NULL,
        url TEXT NOT NULL,
        is_favorite BOOLEAN NOT NULL,
        date_created DATETIME,
        last_modified TEXT,
        tag_id INTEGER,
        folder_id INTEGER,
        FOREIGN KEY(tag_id) REFERENCES tags(id),
        FOREIGN KEY(folder_id) REFERENCES folders(id)
    );
    ''')

    # Create tags table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_name TEXT NOT NULL
    );
    ''')

    # Create folders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS folders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder_name TEXT NOT NULL,
        parent_folder_name TEXT,
        FOREIGN KEY(parent_folder_name) REFERENCES folders(folder_name)
    );
    ''')

    # Create notes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_name TEXT NOT NULL,
        note_path TEXT NOT NULL,
        tag_id INTEGER,
        date_created DATETIME,
        last_modified TEXT,
        FOREIGN KEY(tag_id) REFERENCES tags(id),
        FOREIGN KEY(last_modified) REFERENCES notes(note_path)
    );
    ''')

    # Create user_credentials table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT NOT NULL,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        date_created DATETIME,
        last_modified TEXT,
        FOREIGN KEY(last_modified) REFERENCES user_credentials(password)
    );
    ''')

    # Create app_password table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS app_password (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL
    );
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and tables created successfully!")


# Run the function to create the database and tables
if __name__ == '__main__':
    create_database()