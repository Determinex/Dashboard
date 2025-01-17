from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import datetime

app = Flask(__name__)

def format_size(size):
    """Format the size of the file for display."""
    if size < 1024:
        return f"{size:.2f} Bytes"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    elif size < 1024 ** 4:
        return f"{size / (1024 ** 3):.2f} GB"
    else:
        return f"{size / (1024 ** 4):.2f} TB"

def get_directory_contents(path):
    """Get the contents of a directory."""
    contents = []
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                contents.append({
                    'name': entry.name,
                    'path': entry.path,
                    'type': 'directory'
                })
            else:
                contents.append({
                    'name': entry.name,
                    'path': entry.path,
                    'type': 'file',
                    'size': format_size(entry.stat().st_size),
                    'modified': datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime('%m/%d/%Y'),
                    'encrypted': 'No'  # Placeholder for encryption status
                })
    except Exception as e:
        print(f"Error accessing {path}: {e}")
    return contents

@app.route('/')
def index():
    """Serve the main directory listing."""
    base_directory = '.'  # Change this to your target directory
    tree = get_directory_contents(base_directory)
    return render_template('index.html', tree=tree)

@app.route('/expand')
def expand():
    """Expand a directory to show its contents."""
    path = request.args.get('path')
    contents = get_directory_contents(path)
    return jsonify(contents)

@app.route('/files/<path:filename>')
def serve_file(filename):
    """Serve a file from the directory."""
    base_directory = '.'  # Change this to your target directory
    return send_from_directory(base_directory, filename)

if __name__ == '__main__':
    app.run(debug=True)