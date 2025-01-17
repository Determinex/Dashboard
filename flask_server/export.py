# export.py
import json
import os
from db import BookmarkManager
from logger import Logger

class ExportManager:
    def __init__(self):
        self.db_manager = BookmarkManager()
        self.logger = Logger()

    def export_to_format(self, format_type):
        if format_type == 'chrome':
            self.export_to_chrome()
        elif format_type == 'firefox':
            self.export_to_firefox()
        else:
            self.logger.log_error(f"Unsupported export format: {format_type}")

    def export_to_chrome(self):
        try:
            bookmarks = self.db_manager.get_all_bookmarks()
            chrome_bookmarks = {
                "checksum": "",
                "roots": {
                    "bookmark_bar": {
                        "children": [],
                        "date_modified": 0,
                        "id": "1",
                        "name": "Bookmark Bar",
                        "type": "folder"
                    }
                },
                "version": 1
            }

            for bookmark in bookmarks:
                chrome_bookmarks['roots']['bookmark_bar']['children'].append({
                    "date_added": 0,
                    "id": str(len(chrome_bookmarks['roots']['bookmark_bar']['children'])),
                    "name": bookmark[1],
                    "type": "url",
                    "url": bookmark[2]
                })

            chrome_export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ChromeBookmarks.json')
            with open(chrome_export_path, 'w') as f:
                json.dump(chrome_bookmarks, f, indent=4)
        except Exception as e:
            self.logger.log_error(f"Failed to export bookmarks to Chrome: {e}")

    def export_to_firefox(self):
        try:
            bookmarks = self.db_manager.get_all_bookmarks()
            html_content = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file. It will be overwritten. -->
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
            <DL><p>'''

            for bookmark in bookmarks:
                html_content += f'<DT><A HREF="{bookmark[2]}" ADD_DATE="0" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="false">{bookmark[1]}</A>\n'

            html_content += '''</DL><p>'''
            firefox_export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FirefoxBookmarks.html')
            with open(firefox_export_path, 'w') as f:
                f.write(html_content)
        except Exception as e:
            self.logger.log_error(f"Failed to export bookmarks to Firefox: {e}")

    def export_selected(self, selected_bookmarks):
        try:
            chrome_bookmarks = {
                "checksum": "",
                "roots": {
                    "bookmark_bar": {
                        "children": [],
                        "date_modified": 0,
                        "id": "1",
                        "name": "Bookmark Bar",
                        "type": "folder"
                    }
                },
                "version": 1
            }

            for title, url in selected_bookmarks:
                chrome_bookmarks['roots']['bookmark_bar']['children'].append({
                    "date_added": 0,
                    "id": str(len(chrome_bookmarks['roots']['bookmark_bar']['children'])),
                    "name": title,
                    "type": "url",
                    "url": url
                })

            chrome_export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SelectedChromeBookmarks.json')
            with open(chrome_export_path, 'w') as f:
                json.dump(chrome_bookmarks, f, indent=4)
        except Exception as e:
            self.logger.log_error(f"Failed to export selected bookmarks to Chrome: {e}")
