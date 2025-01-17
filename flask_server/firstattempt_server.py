from flask import Flask, send_from_directory, render_template, request
import os

app = Flask(__name__, template_folder='template')

def generate_directory_tree(root_dir, current_dir=''):
    directory_tree = ''
    for root, dirs, files in os.walk(os.path.join(root_dir, current_dir)):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), root_dir)
            directory_tree += f'<a href="/{file_path}" class="playlist-item">{file}</a><br>'
    return directory_tree

@app.route('/')
def index():
    current_dir = request.args.get('dir', '')
    directory_tree = generate_directory_tree('.', current_dir)
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Directory Tree</title>
    </head>
    <body>
        <h1>Directory Tree</h1>
        {directory_tree}
    </body>
    </html>
    """
    return html

@app.route('/audioPlayer')
def audio_player():
    return render_template('audioPlayer.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)