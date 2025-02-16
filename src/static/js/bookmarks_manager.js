// src/static/js/bookmarks_manager.js

document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('importBookmark').addEventListener('click', showImportExportModal);
    document.getElementById('exportBookmark').addEventListener('click', showImportExportModal);
    document.getElementById('submitImportExport').addEventListener('click', handleImportExport);
    document.getElementById('searchBar').addEventListener('keypress', handleSearch);
    setupDeleteBookmarkListeners();
    setupDeleteFolderListeners();
}

function showImportExportModal() {
    var modal = new bootstrap.Modal(document.getElementById('importExportModal'));
    modal.show();
}

function handleImportExport() {
    var fileInput = document.getElementById('fileInput').files[0];
    var exportFormat = document.getElementById('exportFormat').value;

    // Implement AJAX calls or form submissions to handle the import/export process
    // Example: send fileInput and exportFormat to the server

    var modal = bootstrap.Modal.getInstance(document.getElementById('importExportModal'));
    modal.hide();
}

function handleSearch(e) {
    if (e.key === 'Enter') {
        var query = this.value;
        // Implement AJAX call to search bookmarks based on the query
    }
}

function setupDeleteBookmarkListeners() {
    document.querySelectorAll('.delete-bookmark').forEach(button => {
        button.addEventListener('click', function() {
            const bookmarkId = this.parentElement.getAttribute('data-id');
            fetch(`/bookmarks/${bookmarkId}`, { method: 'DELETE' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.parentElement.remove();
                    }
                });
        });
    });
}

function setupDeleteFolderListeners() {
    document.querySelectorAll('.delete-folder').forEach(button => {
        button.addEventListener('click', function() {
            const folderId = this.parentElement.getAttribute('data-id');
            fetch(`/folders/${folderId}`, { method: 'DELETE' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.parentElement.remove();
                    }
                });
        });
    });
}

function addBookmark() {
    var bookmarkName = document.getElementById('bookmarkName').value;
    var bookmarkUrl = document.getElementById('bookmarkUrl').value;
    var folderId = document.getElementById('folderSelect').value;

    fetch('/bookmarks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: bookmarkName, url: bookmarkUrl, folder_id: folderId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add the new bookmark to the UI
            var bookmarksList = document.getElementById('bookmarksList');
            var newBookmark = document.createElement('div');
            newBookmark.className = 'bookmark-item';
            newBookmark.setAttribute('data-id', data.id);
            newBookmark.innerHTML = `<span>${bookmarkName}</span><button class="delete-bookmark">Delete</button>`;
            bookmarksList.appendChild(newBookmark);
            setupDeleteBookmarkListeners(); // Re-setup listeners for the new bookmark
        }
    });
}

function addFolder() {
    var folderName = document.getElementById('folderName').value;

    fetch('/folders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: folderName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add the new folder to the UI
            var foldersList = document.getElementById('foldersList');
            var newFolder = document.createElement('div');
            newFolder.className = 'folder-item';
            newFolder.setAttribute('data-id', data.id);
            newFolder.innerHTML = `<span>${folderName}</span><button class="delete-folder">Delete</button>`;
            foldersList.appendChild(newFolder);
            setupDeleteFolderListeners(); // Re-setup listeners for the new folder
        }
    });
}

function editBookmark(bookmarkId) {
    var bookmarkName = document.getElementById('editBookmarkName').value;
    var bookmarkUrl = document.getElementById('editBookmarkUrl').value;

    fetch(`/bookmarks/${bookmarkId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: bookmarkName, url: bookmarkUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the bookmark in the UI
            var bookmarkItem = document.querySelector(`.bookmark-item[data-id="${bookmarkId}"]`);
            bookmarkItem.querySelector('span').textContent = bookmarkName;
        }
    });
}

function editFolder(folderId) {
    var folderName = document.getElementById('editFolderName').value;

    fetch(`/folders/${folderId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: folderName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the folder in the UI
            var folderItem = document.querySelector(`.folder-item[data-id="${folderId}"]`);
            folderItem.querySelector('span').textContent = folderName;
        }
    });
}

function sortBookmarks() {
    var bookmarksList = document.getElementById('bookmarksList');
    var bookmarks = Array.from(bookmarksList.children);

    bookmarks.sort((a, b) => {
        var nameA = a.querySelector('span').textContent.toLowerCase();
        var nameB = b.querySelector('span').textContent.toLowerCase();
        return nameA.localeCompare(nameB);
    });

    bookmarks.forEach(bookmark => bookmarksList.appendChild(bookmark));
}

function sortFolders() {
    var foldersList = document.getElementById('foldersList');
    var folders = Array.from(foldersList.children);

    folders.sort((a, b) => {
        var nameA = a.querySelector('span').textContent.toLowerCase();
        var nameB = b.querySelector('span').textContent.toLowerCase();
        return nameA.localeCompare(nameB);
    });

    folders.forEach(folder => foldersList.appendChild(folder));
}

function toggleBookmarkVisibility() {
    var bookmarksList = document.getElementById('bookmarksList');
    bookmarksList.classList.toggle('hidden');
}

function toggleFolderVisibility() {
    var foldersList = document.getElementById('foldersList');
    foldersList.classList.toggle('hidden');
}

function toggleBookmarkEditMode() {
    var bookmarksList = document.getElementById('bookmarksList');
    bookmarksList.classList.toggle('edit-mode');
}

function toggleFolderEditMode() {
    var foldersList = document.getElementById('foldersList');
    foldersList.classList.toggle('edit-mode');
}

function toggleBookmarkSortMode() {
    var bookmarksList = document.getElementById('bookmarksList');
    bookmarksList.classList.toggle('sort-mode');
}

function toggleFolderSortMode() {
    var foldersList = document.getElementById('foldersList');
    foldersList.classList.toggle('sort-mode');
}

function toggleBookmarkSearchMode() {
    var searchBar = document.getElementById('searchBar');
    searchBar.classList.toggle('search-mode');
}

function toggleFolderSearchMode() {
    var searchBar = document.getElementById('searchBar');
    searchBar.classList.toggle('search-mode');
}

function toggleBookmarkImportExportMode() {
    var importExportModal = document.getElementById('importExportModal');
    importExportModal.classList.toggle('show');
}

function toggleFolderImportExportMode() {
    var importExportModal = document.getElementById('importExportModal');
    importExportModal.classList.toggle('show');
}

function toggleBookmarkAddMode() {
    var addBookmarkModal = document.getElementById('addBookmarkModal');
    addBookmarkModal.classList.toggle('show');
}

function toggleFolderAddMode() {
    var addFolderModal = document.getElementById('addFolderModal');
    addFolderModal.classList.toggle('show');
}

function toggleBookmarkEditMode() {
    var editBookmarkModal = document.getElementById('editBookmarkModal');
    editBookmarkModal.classList.toggle('show');
}

function toggleFolderEditMode() {
    var editFolderModal = document.getElementById('editFolderModal');
    editFolderModal.classList.toggle('show');
}

function toggleBookmarkSortMode() {
    var sortBookmarkModal = document.getElementById('sortBookmarkModal');
    sortBookmarkModal.classList.toggle('show');
}

function toggleFolderSortMode() {
    var sortFolderModal = document.getElementById('sortFolderModal');
    sortFolderModal.classList.toggle('show');
}

function toggleBookmarkSearchMode() {
    var searchBar = document.getElementById('searchBar');
    searchBar.classList.toggle('show');
}

function toggleFolderSearchMode() {
    var searchBar = document.getElementById('searchBar');
    searchBar.classList.toggle('show');
}

function toggleBookmarkImportExportMode() {
    var importExportModal = document.getElementById('importExportModal');
    importExportModal.classList.toggle('show');
}

function toggleFolderImportExportMode() {
    var importExportModal = document.getElementById('importExportModal');
    importExportModal.classList.toggle('show');
}

function toggleBookmarkAddMode() {
    var addBookmarkModal = document.getElementById('addBookmarkModal');
    addBookmarkModal.classList.toggle('show');
}

function toggleFolderAddMode() {
    var addFolderModal = document.getElementById('addFolderModal');
    addFolderModal.classList.toggle('show');
}

function toggleBookmarkEditMode() {
    var editBookmarkModal = document.getElementById('editBookmarkModal');
    editBookmarkModal.classList.toggle('show');
}

function toggleFolderEditMode() {
    var editFolderModal = document.getElementById('editFolderModal');
    editFolderModal.classList.toggle('show');
}

function toggleBookmarkSortMode() {
    var sortBookmarkModal = document.getElementById('sortBookmarkModal');
    sortBookmarkModal.classList.toggle('show');
}