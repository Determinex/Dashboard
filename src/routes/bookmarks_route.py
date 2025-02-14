from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from src.models import db, Bookmark, Folder, Tag
from src.auth.forms import BookmarkForm

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/bookmarks_manager', methods=['GET', 'POST'])
@login_required
def bookmarks_manager():
    folders = Folder.query.all()
    tags = Tag.query.all()
    bookmarks = Bookmark.query.all()
    form = BookmarkForm()

    # Populate the form choices
    form.folder_id.choices = [(folder.id, folder.name) for folder in folders]
    form.tag_id.choices = [(tag.id, tag.name) for tag in tags]

    if request.method == 'POST':
        # Handle bookmark creation
        title = request.form['title']
        url = request.form['url']
        folder_id = request.form.get('folder_id', type=int)
        tag_id = request.form.get('tag_id', type=int)

        new_bookmark = Bookmark(title=title, url=url, folder_id=folder_id, tag_id=tag_id)
        db.session.add(new_bookmark)
        db.session.commit()
        return jsonify(success=True)

    return render_template('bookmarks_manager.html', bookmarks=bookmarks, form=form)

@bookmarks_bp.route('/bookmarks/<int:bookmark_id>', methods=['DELETE'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify(success=True)

@bookmarks_bp.route('/edit_bookmark/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    form = BookmarkForm(obj=bookmark)

    if request.method == 'POST':
        form.populate_obj(bookmark)
        db.session.commit()
        return jsonify(success=True)

    return render_template('edit_bookmark.html', form=form, bookmark=bookmark)

@bookmarks_bp.route('/get_bookmark/<int:bookmark_id>', methods=['GET'])
@login_required
def get_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    return jsonify(title=bookmark.title, url=bookmark.url, folder_id=bookmark.folder_id, tag_id=bookmark.tag_id)

@bookmarks_bp.route('/get_bookmarks', methods=['GET'])
@login_required
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    return jsonify(bookmarks=[bookmark.to_dict() for bookmark in bookmarks])

@bookmarks_bp.route('/get_folders', methods=['GET'])
@login_required
def get_folders():
    folders = Folder.query.all()
    return jsonify(folders=[folder.to_dict() for folder in folders])

@bookmarks_bp.route('/get_tags', methods=['GET'])
@login_required
def get_tags():
    tags = Tag.query.all()
    return jsonify(tags=[tag.to_dict() for tag in tags])

@bookmarks_bp.route('/get_bookmark_by_folder/<int:folder_id>', methods=['GET'])
@login_required
def get_bookmark_by_folder(folder_id):
    bookmarks = Bookmark.query.filter_by(folder_id=folder_id).all()
    return jsonify(bookmarks=[bookmark.to_dict() for bookmark in bookmarks])

@bookmarks_bp.route('/get_bookmark_by_tag/<int:tag_id>', methods=['GET'])
@login_required
def get_bookmark_by_tag(tag_id):
    bookmarks = Bookmark.query.filter_by(tag_id=tag_id).all()
    return jsonify(bookmarks=[bookmark.to_dict() for bookmark in bookmarks])

@bookmarks_bp.route('/get_bookmark_by_folder_and_tag/<int:folder_id>/<int:tag_id>', methods=['GET'])
@login_required
def get_bookmark_by_folder_and_tag(folder_id, tag_id):
    bookmarks = Bookmark.query.filter_by(folder_id=folder_id, tag_id=tag_id).all()
    return jsonify(bookmarks=[bookmark.to_dict() for bookmark in bookmarks])

@bookmarks_bp.route('/get_bookmark_by_folder_or_tag/<int:folder_id>/<int:tag_id>', methods=['GET'])
@login_required
def get_bookmark_by_folder_or_tag(folder_id, tag_id):
    bookmarks = Bookmark.query.filter((Bookmark.folder_id == folder_id) | (Bookmark.tag_id == tag_id)).all()
    return jsonify(bookmarks=[bookmark.to_dict() for bookmark in bookmarks])