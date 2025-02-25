# browser.py
from browser_history import get_history
from logger import Logger

class BrowserManager:
    def __init__(self):
        self.logger = Logger()

    def fetch_bookmarks(self):
        try:
            history = get_history()
            bookmarks = [(entry.title, entry.url) for entry in history.entries]
            return bookmarks
        except Exception as e:
            self.logger.log_error(f"Failed to fetch browser history: {e}")
            return []

    def filter_bookmarks(self, bookmarks, query):
        return [bookmark for bookmark in bookmarks if query.lower() in bookmark[0].lower()]