# main.py
from db import BookmarkManager, FolderManager
from browser import BrowserManager
from export import ExportManager
from generate import WebPageGenerator
from settings_manager import SettingsManager
from logger import Logger
from gui import BookmarkManagerGUI
import tkinter as tk

class BookmarkManagerApp:
    def __init__(self):
        self.bookmark_manager = BookmarkManager()
        self.folder_manager = FolderManager()
        self.browser_manager = BrowserManager()
        self.export_manager = ExportManager()
        self.webpage_generator = WebPageGenerator()
        self.settings_manager = SettingsManager()

    def run(self):
        root = tk.Tk()
        app = BookmarkManagerGUI(root)
        root.mainloop()

if __name__ == "__main__":
    app = BookmarkManagerApp()
    app.run()