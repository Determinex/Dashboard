from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from .models import Bookmark, Tag, BookmarkTag, Directory
from app import db
import os

blueprint = Blueprint(
    'bookmarks',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/bookmarks/static'
)

@blueprint.route('/bookmarks')
@login_required
def bookmarks():
    """Render the bookmarks page."""
    return render_template('bookmarks.html')

@blueprint.route('/api/bookmarks', methods=['GET', 'POST'])
@login_required
@cross_origin()
def api_bookmarks():
    """Handle API requests for bookmarks."""
    if request.method == 'POST':
        data = request.json

        # Handle tags: Retrieve existing tags or create new ones
        tags = []
        existing_tags = {tag.name: tag for tag in Tag.query.filter(Tag.name.in_(data['tags'])).all()}
        for tag_name in data['tags']:
            if tag_name in existing_tags:
                tags.append(existing_tags[tag_name])
            else:
                new_tag = Tag(name=tag_name)
                db.session.add(new_tag)
                db.session.flush()  # Flush to ensure the tag is available for the relationship
                tags.append(new_tag)

        # Handle directory: Retrieve existing directory or create a new one
        directory = None
        directory_id = None
        if data['directory']:
            directory = Directory.query.filter_by(name=data['directory']).first()
            if not directory:
                directory = Directory(name=data['directory'])
                db.session.add(directory)
                db.session.flush()  # Flush to ensure the directory ID is available
            directory_id = directory.id

        # Create the new bookmark
        new_bookmark = Bookmark(
            user_id=current_user.id,
            url=data['url'],
            title=data['title'],
            description=data.get('description', ''),  # Add description field
            tags=tags,
            directory_id=directory_id  # Use directory_id instead of directory
        )
        db.session.add(new_bookmark)
        db.session.commit()

        # Save the bookmark to a user-specific file
        user_dir = os.path.join('user_data', current_user.uuid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        with open(os.path.join(user_dir, 'bookmarks.txt'), 'a') as f:
            f.write(f"{new_bookmark.title} - {new_bookmark.url}\n")

        return jsonify({'message': 'Bookmark added!'})

    # Handle GET request: Return all bookmarks for the current user
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    return jsonify([bookmark.to_dict() for bookmark in bookmarks])

@blueprint.route('/api/bookmarks/<int:id>', methods=['DELETE'])
@login_required
@cross_origin()
def delete_bookmark(id):
    """Handle API requests to delete a bookmark."""
    bookmark = Bookmark.query.get_or_404(id)
    if bookmark.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    # Explicitly delete associated rows in the BookmarkTag table
    BookmarkTag.query.filter_by(bookmark_id=bookmark.id).delete()

    db.session.delete(bookmark)
    db.session.commit()

    # Remove the bookmark from the user's file
    user_dir = os.path.join('user_data', current_user.uuid)
    bookmarks_file = os.path.join(user_dir, 'bookmarks.txt')
    if os.path.exists(bookmarks_file):
        with open(bookmarks_file, 'r') as f:
            lines = f.readlines()
        with open(bookmarks_file, 'w') as f:
            for line in lines:
                if f"{bookmark.title} - {bookmark.url}" not in line:
                    f.write(line)

    return jsonify({'message': 'Bookmark deleted!'})

@blueprint.route('/api/bookmarks/<int:id>', methods=['PUT'])
@login_required
@cross_origin()
def update_bookmark(id):
    """Handle API requests to update a bookmark."""
    bookmark = Bookmark.query.get_or_404(id)
    if bookmark.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    bookmark.title = data['title']
    bookmark.url = data['url']
    bookmark.description = data.get('description', '')  # Update description field
    bookmark.tags = [Tag.query.filter_by(name=tag).first() or Tag(name=tag) for tag in data['tags']]
    bookmark.directory = Directory.query.filter_by(name=data['directory']).first()
    db.session.commit()
    return jsonify({'message': 'Bookmark updated!'})

@blueprint.route('/api/tags', methods=['GET', 'POST'])
@login_required
@cross_origin()
def api_tags():
    """Handle API requests for tags."""
    if request.method == 'POST':
        data = request.json
        # Check if the tag already exists
        tag = Tag.query.filter_by(name=data['name']).first()
        if not tag:
            # Create a new tag if it doesn't exist
            tag = Tag(name=data['name'])
            db.session.add(tag)
            db.session.commit()
            return jsonify({'message': 'Tag added!'})
        return jsonify({'message': 'Tag already exists!'})

    # Handle GET request: Return all tags
    tags = Tag.query.all()
    return jsonify([tag.name for tag in tags])

@blueprint.route('/api/directories', methods=['GET', 'POST'])
@login_required
@cross_origin()
def api_directories():
    """Handle API requests for directories."""
    if request.method == 'POST':
        data = request.json
        # Check if the directory already exists
        directory = Directory.query.filter_by(name=data['name']).first()
        if not directory:
            # Create a new directory if it doesn't exist
            parent_id = data.get('parent_id')
            directory = Directory(name=data['name'], parent_id=parent_id)
            db.session.add(directory)
            db.session.commit()
            return jsonify({'message': 'Directory added!'})
        return jsonify({'message': 'Directory already exists!'})

    # Handle GET request: Return all directories
    directories = Directory.query.all()
    return jsonify([directory.to_dict() for directory in directories])