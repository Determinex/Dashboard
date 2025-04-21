import logging
from flask import Flask, request, jsonify, render_template, Blueprint
from jsonschema import validate, ValidationError
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///bookmarks.db')
Session = sessionmaker(bind=engine)

# Define models
class Directory(Base):
    __tablename__ = 'directories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False, nullable=True, unique=True)
    parent_id = Column(Integer, ForeignKey('directories.id'), nullable=True)
    parent = relationship("Directory", remote_side=[id], backref="subdirectories")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    directory_id = Column(Integer, ForeignKey('directories.id'))
    is_favorite = Column(Boolean, default=False)
    directory = relationship("Directory", back_populates="bookmarks")
    tags = relationship("Tag", secondary="bookmark_tags", back_populates="bookmarks")

Directory.bookmarks = relationship("Bookmark", order_by=Bookmark.id, back_populates="directory")
Tag.bookmarks = relationship("Bookmark", secondary="bookmark_tags", back_populates="tags")

# Create database tables
Base.metadata.create_all(engine)

# Define the bookmarks schema
bookmarks_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Name": {"type": "string"},
        "URL": {"type": "string"},
        "Description": {"type": "string"},
        "TagName": {"type": "array", "items": {"type": "string"}},
        "DirectoryName": {"type": "string"},
        "IsFavorite": {"type": "boolean"}
    },
    "required": ["Name", "URL"]
}

# Context manager for database session
def get_session():
    """Context manager for database session."""
    session = Session()
    try:
        yield session
    finally:
        session.close()

# Define the Bookmark Manager Blueprint
bmBP = Blueprint('bmBP', __name__)

@bmBP.route('/')
def index():
    with get_session() as session:
        bookmarks = fetch_bookmarks(session)
        directories = fetch_directories(session)
        return render_template('bookmark_manager.html', bookmarks=bookmarks, directories=directories)

# Define the Bookmark Manager API Blueprint
bmAPI = Blueprint('bmAPI', __name__)

@bmAPI.route('/bookmarks', methods=['GET', 'POST'])
def handle_bookmarks():
    with get_session() as session:
        if request.method == 'POST':
            data = request.json
            if not isinstance(data, list):
                return jsonify({"error": "Payload must be a list of bookmarks."}), 400

            errors = []
            for bookmark_data in data:
                try:
                    validate(instance=bookmark_data, schema=bookmarks_schema)
                    directory_name = bookmark_data.get('DirectoryName')
                    directory = session.query(Directory).filter_by(name=directory_name).first() if directory_name else None
                    if directory is None and directory_name:
                        directory = Directory(name=directory_name)
                        session.add(directory)

                    existing_bookmark = session.query(Bookmark).filter_by(url=bookmark_data['URL']).first()
                    if existing_bookmark:
                        existing_bookmark.name = bookmark_data['Name']
                        existing_bookmark.description = bookmark_data.get('Description')
                        existing_bookmark.directory = directory
                        existing_bookmark.is_favorite = bookmark_data.get('IsFavorite', False)
                    else:
                        new_bookmark = Bookmark(
                            name=bookmark_data['Name'],
                            url=bookmark_data['URL'],
                            description=bookmark_data.get('Description'),
                            directory=directory,
                            is_favorite=bookmark_data.get('IsFavorite', False)
                        )
                        session.add(new_bookmark)

                    tags = bookmark_data.get('TagName', [])
                    for tag_name in tags:
                        tag = session.query(Tag).filter_by(name=tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            session.add(tag)
                        if tag not in new_bookmark.tags:
                            new_bookmark.tags.append(tag)

                except ValidationError as e:
                    errors.append({"errors": e.message})
                except IntegrityError:
                    session.rollback()
                    errors.append({"error": "Database integrity error."})

            if errors:
                return jsonify({"errors": errors}), 400

            session.commit()
            return jsonify({"message": "Bookmarks processed successfully."}), 201

        elif request.method == 'GET':
            bookmarks = session.query(Bookmark).all()
            bookmarks_list = [
                {
                    "Name": b.name,
                    "URL": b.url,
                    "Description": b.description,
                    "DirectoryName": b.directory.name if b.directory else None,
                    "TagName": [tag.name for tag in b.tags],
                    "IsFavorite": b.is_favorite
                }
                for b in bookmarks
            ]
            return jsonify(bookmarks_list), 200

@bmAPI.route('/directories', methods=['GET', 'POST'])
def handle_directories():
    with get_session() as session:
        if request.method == 'GET':
            directories = session.query(Directory).all()
            return jsonify([{"id": d.id, "name": d.name, "is_default": d.is_default} for d in directories]), 200

        elif request.method == 'POST':
            data = request.json
            new_directory = Directory(name=data['name'], is_default=data.get('is_default', False))

            if new_directory.is_default:
                session.query(Directory).filter(Directory.is_default == True).update({"is_default": False})

            session.add(new_directory)
            session.commit()
            return jsonify({"message": "Directory created successimport logging
from flask import Flask, request, jsonify, render_template, Blueprint
from flask_cors import CORS
from jsonschema import validate, ValidationError
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///bookmarks.db')
Session = sessionmaker(bind=engine)

# Define models
class Directory(Base):
    __tablename__ = 'directories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False, nullable=True, unique=True)
    parent_id = Column(Integer, ForeignKey('directories.id'), nullable=True)
    parent = relationship("Directory", remote_side=[id], backref="subdirectories")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    directory_id = Column(Integer, ForeignKey('directories.id'))
    is_favorite = Column(Boolean, default=False)
    directory = relationship("Directory", back_populates="bookmarks")
    tags = relationship("Tag", secondary="bookmark_tags", back_populates="bookmarks")

Directory.bookmarks = relationship("Bookmark", order_by=Bookmark.id, back_populates="directory")
Tag.bookmarks = relationship("Bookmark", secondary="bookmark_tags", back_populates="tags")

# Create database tables
Base.metadata.create_all(engine)

# Define the bookmarks schema
bookmarks_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Name": {"type": "string"},
        "URL": {"type": "string"},
        "Description": {"type": "string"},
        "TagName": {"type": "array", "items": {"type": "string"}},
        "DirectoryName": {"type": "string"},
        "IsFavorite": {"type": "boolean"}
    },
    "required": ["Name", "URL"]
}

# Context manager for database session
def get_session():
    """Context manager for database session."""
    session = Session()
    try:
        yield session
    finally:
        session.close()

# Define the Bookmark Manager Blueprint
bmBP = Blueprint('bmBP', __name__)

@bmBP.route('/')
def index():
    with get_session() as session:
        bookmarks = fetch_bookmarks(session)
        directories = fetch_directories(session)
        return render_template('bookmark_manager.html', bookmarks=bookmarks, directories=directories)

# Define the Bookmark Manager API Blueprint
bmAPI = Blueprint('bmAPI', __name__)

@bmAPI.route('/bookmarks', methods=['GET', 'POST'])
def handle_bookmarks():
    with get_session() as session:
        if request.method == 'POST':
            data = request.json
            if not isinstance(data, list):
                return jsonify({"error": "Payload must be a list of bookmarks."}), 400

            errors = []
            for bookmark_data in data:
                try:
                    validate(instance=bookmark_data, schema=bookmarks_schema)
                    directory_name = bookmark_data.get('DirectoryName')
                    directory = session.query(Directory).filter_by(name=directory_name).first() if directory_name else None
                    if directory is None and directory_name:
                        directory = Directory(name=directory_name)
                        session.add(directory)

                    existing_bookmark = session.query(Bookmark).filter_by(url=bookmark_data['URL']).first()
                    if existing_bookmark:
                        existing_bookmark.name = bookmark_data['Name']
                        existing_bookmark.description = bookmark_data.get('Description')
                        existing_bookmark.directory = directory
                        existing_bookmark.is_favorite = bookmark_data.get('IsFavorite', False)
                    else:
                        new_bookmark = Bookmark(
                            name=bookmark_data['Name'],
                            url=bookmark_data['URL'],
 description=bookmark_data.get('Description'),
                            directory=directory,
                            is_favorite=bookmark_data.get('IsFavorite', False)
                        )
                        session.add(new_bookmark)

                    tags = bookmark_data.get('TagName', [])
                    for tag_name in tags:
                        tag = session.query(Tag).filter_by(name=tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            session.add(tag)
                        if tag not in new_bookmark.tags:
                            new_bookmark.tags.append(tag)

                except ValidationError as e:
                    errors.append({"errors": e.message})
                except IntegrityError:
                    session.rollback()
                    errors.append({"error": "Database integrity error."})

            if errors:
                return jsonify({"errors": errors}), 400

            session.commit()
            return jsonify({"message": "Bookmarks processed successfully."}), 201

        elif request.method == 'GET':
            bookmarks = session.query(Bookmark).all()
            bookmarks_list = [
                {
                    "Name": b.name,
                    "URL": b.url,
                    "Description": b.description,
                    "DirectoryName": b.directory.name if b.directory else None,
                    "TagName": [tag.name for tag in b.tags],
                    "IsFavorite": b.is_favorite
                }
                for b in bookmarks
            ]
            return jsonify(bookmarks_list), 200

@bmAPI.route('/directories', methods=['GET', 'POST'])
def handle_directories():
    with get_session() as session:
        if request.method == 'GET':
            directories = session.query(Directory).all()
            return jsonify([{"id": d.id, "name": d.name, "is_default": d.is_default} for d in directories]), 200

        elif request.method == 'POST':
            data = request.json
            new_directory = Directory(name=data['name'], is_default=data.get('is_default', False))

            if new_directory.is_default:
                session.query(Directory).filter(Directory.is_default == True).update({"is_default": False})

            session.add(new_directory)
            session.commit()
            return jsonify({"message": "Directory created successfully."}), 201

@bmAPI.route('/bookmarks/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    with get_session() as session:
        bookmark = session.query(Bookmark).get(bookmark_id)
        if not bookmark:
            return jsonify({"error": "Bookmark not found."}), 404
        session.delete(bookmark)
        session.commit()
        return jsonify({"message": "Bookmark deleted successfully."}), 200

@bmAPI.route('/bookmarks/move', methods=['PUT'])
def move_bookmark():
    with get_session() as session:
        data = request.json
        bookmark = session.query(Bookmark).get(data['bookmark_id'])
        if not bookmark:
            return jsonify({"error": "Bookmark not found."}), 404
        bookmark.directory_id = data['new_directory_id']
        session.commit()
        return jsonify({"message": "Bookmark moved successfully."}), 200

# Helper functions
def fetch_bookmarks(session):
    return [
        {
            "Name": b.name,
            "URL": b.url,
            "Description": b.description,
            "DirectoryName": b.directory.name if b.directory else None,
            "TagName": [tag.name for tag in b.tags],
            "IsFavorite": b.is_favorite
        }
        for b in session.query(Bookmark).all()
    ]

def fetch_directories(session):
    return [{"id": d.id, "name": d.name, "is_default": d.is_default} for d in session.query(Directory).all()]

# Register blueprints
# app.register_blueprint(bmBP)
# app.register_blueprint(bmAPI, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)fully."}), 201

@bmAPI.route('/bookmarks/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    with get_session() as session:
        bookmark = session.query(Bookmark).get(bookmark_id)
        if not bookmark:
            return jsonify({"error": "Bookmark not found."}), 404
        session.delete(bookmark)
        session.commit()
        return jsonify({"message": "Bookmark deleted successfully."}), 200

@bmAPI.route('/bookmarks/move', methods=['PUT'])
def move_bookmark():
    with get_session() as session:
        data = request.json
        bookmark = session.query(Bookmark).get(data['bookmark_id'])
        if not bookmark:
            return jsonify({"error": "Bookmark not found."}), 404
        bookmark.directory_id = data['new_directory_id']
        session.commit()
        return jsonify({"message": "Bookmark moved successfully."}), 200

# Helper functions
def fetch_bookmarks(session):
    return [
        {
            "Name": b.name,
            "URL": b.url,
            "Description": b.description,
            "DirectoryName": b.directory.name if b.directory else None,
            "TagName": [tag.name for tag in b.tags],
            "IsFavorite": b.is_favorite
        }
        for b in session.query(Bookmark).all()
    ]

def fetch_directories(session):
    return [{"id": d.id, "name": d.name, "is_default": d.is_default} for d in session.query(Directory).all()]

# Register blueprints
# app.register_blueprint(bmBP)
# app.register_blueprint(bmAPI, url_prefix='/api')
