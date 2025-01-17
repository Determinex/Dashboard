# gui.py
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from db import BookmarkManager
from export import ExportManager
from generate import WebPageGenerator

class BookmarkManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookmark Manager")

        self.bookmark_manager = BookmarkManager()
        self.export_manager = ExportManager()
        self.webpage_generator = WebPageGenerator()

        self.create_widgets()
        self.populate_bookmarks()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.label = tk.Label(self.frame, text="Bookmark Title:")
        self.label.grid(row=0, column=0)

        self.title_entry = tk.Entry(self.frame, width=30)
        self.title_entry.grid(row=0, column=1)

        self.label_url = tk.Label(self.frame, text="Bookmark URL:")
        self.label_url.grid(row=1, column=0)

        self.url_entry = tk.Entry(self.frame, width=30)
        self.url_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame, text="Add Bookmark", command=self.add_bookmark)
        self.add_button.grid(row=2, column=0, columnspan=2)

        self.view_button = tk.Button(self.frame, text="View Bookmarks", command=self.populate_bookmarks)
        self.view_button.grid(row=3, column=0, columnspan=2)

        self.export_button = tk.Button(self.frame, text="Export Selected", command=self.export_selected)
        self.export_button.grid(row=4, column=0, columnspan=2)

        self.generate_button = tk.Button(self.frame, text="Generate Webpage", command=self.generate_webpage)
        self.generate_button.grid(row=5, column=0, columnspan=2)

        # Sidebar for displaying bookmarks
        self.sidebar_frame = tk.Frame(self.root)
        self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.bookmark_listbox = Listbox(self.sidebar_frame, selectmode=tk.MULTIPLE, width=50, height=20)
        self.bookmark_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = Scrollbar(self.sidebar_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.bookmark_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.bookmark_listbox.yview)

    def add_bookmark(self):
        title = self.title_entry.get()
        url = self.url_entry.get()
        if self.bookmark_manager.add_bookmark(title, url):
            messagebox.showinfo("Success", "Bookmark added successfully!")
            self.title_entry.delete(0, tk.END)
            self.url_entry.delete(0, tk.END)
            self.populate_bookmarks()
        else:
            messagebox.showerror("Error", "Failed to add bookmark. It may already exist.")

    def populate_bookmarks(self):
        # Clear current listbox
        self.bookmark_listbox.delete(0, tk.END)

        # Fetch and display bookmarks in the listbox
        bookmarks = self.bookmark_manager.get_all_bookmarks()
        for bookmark in bookmarks:
            title = bookmark[1]
            url = bookmark[2]
            folder_id = bookmark[3]
            folder_name = self.bookmark_manager.get_folder_name(folder_id) if folder_id else "No Folder"
            is_favorite = "★" if bookmark[4] else "☆"  # Assuming the 4th index is for favorite status

            # Display format: "[Favorite Status] Title (Folder Name)"
            display_text = f"{is_favorite} {title} (Folder: {folder_name})"
            self.bookmark_listbox.insert(tk.END, display_text)

    def export_selected(self):
        selected_indices = self.bookmark_listbox.curselection()
        selected_bookmarks = []

        for index in selected_indices:
            bookmark_entry = self.bookmark_listbox.get(index)
            title, url = bookmark_entry.split(": ", 1)  # Split title from URL
            selected_bookmarks.append((title.strip(), url.strip()))

        if selected_bookmarks:
            self.export_manager.export_selected(selected_bookmarks)
            messagebox.showinfo("Export", "Selected bookmarks exported successfully!")
        else:
            messagebox.showwarning("Select Bookmarks", "Please select at least one bookmark to export.")

    def generate_webpage(self):
        self.webpage_generator.generate_webpage()  # This will now use the JSON method
        messagebox.showinfo("Webpage", "Bookmarks webpage generated.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookmarkManagerGUI(root)
    root.mainloop()
