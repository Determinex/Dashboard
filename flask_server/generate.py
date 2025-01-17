# generate.py
import os
import json
from db import BookmarkManager
from logger import Logger

class WebPageGenerator:
    def __init__(self):
        self.db_manager = BookmarkManager()
        self.logger = Logger()

    def generate_webpage(self):
        # Fetch bookmarks from the database
        bookmarks = self.db_manager.get_all_bookmarks()
        # Prepare the JSON structure
        json_data = {
            "bookmarks": []
        }

        # Populate the JSON structure
        for bookmark in bookmarks:
            bookmark_entry = {
                "title": bookmark[1],
                "url": bookmark[2],
                "is_favorite": bookmark[4] == 1  # Assuming the 4th index indicates if it's a favorite
            }
            # Check if the folder_id is present and add it to the bookmark entry
            folder_id = bookmark[3]
            if folder_id:
                folder_name = self.db_manager.get_folder_name(folder_id)
                # Add folder structure if it does not exist
                folder_entry = next((folder for folder in json_data['bookmarks'] if folder['title'] == folder_name), None)
                if folder_entry is None:
                    folder_entry = {
                        "title": folder_name,
                        "type": "folder",
                        "children": []
                    }
                    json_data['bookmarks'].append(folder_entry)
                folder_entry['children'].append(bookmark_entry)
            else:
                json_data['bookmarks'].append({
                    "title": "Uncategorized",
                    "type": "folder",
                    "children": [bookmark_entry]
                })

        # Generate the HTML from the JSON structure
        self.generate_webpage_from_json(json_data)

    def generate_webpage_from_json(self, data):
        try:
            html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bookmarks</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        a { text-decoration: none; color: #1a0dab; }
        .favorite { color: red; } /* Style for favorites */
    </style>
</head>
<body>
    <h1>Master List of Bookmarks</h1>
    <ul>
'''

            for folder in data['bookmarks']:
                html_content += f'        <li><strong>{folder["title"]}</strong><ul>\n'
                for bookmark in folder.get('children', []):
                    favorite_class = "favorite" if bookmark['is_favorite'] else ""
                    html_content += f'            <li class="{favorite_class}"><a href="{bookmark["url"]}" target="_blank">{bookmark["title"]}</a></li>\n'
                html_content += '        </ul></li>\n'

            html_content += '''    </ul>
</body>
</html>'''

            html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Bookmarks.html')
            with open(html_file_path, 'w') as f:
                f.write(html_content)

            print("Webpage generated successfully from JSON.")

        except Exception as e:
            self.logger.log_error(f"Failed to generate webpage from JSON: {e}")

# Example usage (comment this out in production code)
# generator = WebPageGenerator()
# generator.generate_webpage()
