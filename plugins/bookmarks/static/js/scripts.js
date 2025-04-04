$(document).ready(function () {
    const contextMenu = $('#custom-context-menu');

    // Show custom context menu
    function showContextMenu(event, options) {
        event.preventDefault();

        // Populate the context menu with options
        contextMenu.find('#edit-item').toggle(options.edit);
        contextMenu.find('#delete-item').toggle(options.delete);
        contextMenu.find('#refresh-area').toggle(options.refreshArea);
        contextMenu.find('#refresh-page').toggle(options.refreshPage);

        // Position the context menu at the cursor's location
        contextMenu.css({
            top: event.pageY + 'px',
            left: event.pageX + 'px',
        }).removeClass('hidden');
    }

    // Hide the context menu
    function hideContextMenu() {
        contextMenu.addClass('hidden');
    }

    // Handle right-click on directory items
    $('#directory-column').on('contextmenu', '.folder-item', function (event) {
        showContextMenu(event, {
            edit: true,
            delete: true,
            refreshArea: true,
            refreshPage: true,
        });

        // Store the clicked item's ID for later use
        contextMenu.data('target-id', $(this).data('id'));
        contextMenu.data('target-type', 'directory');
    });

    // Handle right-click on bookmark items
    $('#display-column').on('contextmenu', '.bookmark-item', function (event) {
        showContextMenu(event, {
            edit: true,
            delete: true,
            refreshArea: true,
            refreshPage: true,
        });

        // Store the clicked item's ID for later use
        contextMenu.data('target-id', $(this).data('id'));
        contextMenu.data('target-type', 'bookmark');
    });

    // Hide the context menu on click elsewhere
    $(document).on('click', function () {
        hideContextMenu();
    });

    // Handle context menu actions
    contextMenu.on('click', '#edit-item', function () {
        const targetId = contextMenu.data('target-id');
        const targetType = contextMenu.data('target-type');

        if (targetType === 'directory') {
            const newName = prompt('Enter new directory name:');
            if (newName) {
                apiRequest(`/api/directories/${targetId}`, 'PUT', { name: newName }, function () {
                    alert('Directory updated successfully.');
                    loadFolderTree();
                });
            }
        } else if (targetType === 'bookmark') {
            const newTitle = prompt('Enter new bookmark title:');
            const newUrl = prompt('Enter new bookmark URL:');
            if (newTitle && newUrl) {
                apiRequest(`/api/bookmarks/${targetId}`, 'PUT', { title: newTitle, url: newUrl }, function () {
                    alert('Bookmark updated successfully.');
                    loadBookmarks();
                });
            }
        }
    });

    contextMenu.on('click', '#delete-item', function () {
        const targetId = contextMenu.data('target-id');
        const targetType = contextMenu.data('target-type');

        if (targetType === 'directory') {
            if (confirm('Are you sure you want to delete this directory?')) {
                apiRequest(`/api/directories/${targetId}`, 'DELETE', null, function () {
                    alert('Directory deleted successfully.');
                    loadFolderTree();
                });
            }
        } else if (targetType === 'bookmark') {
            if (confirm('Are you sure you want to delete this bookmark?')) {
                apiRequest(`/api/bookmarks/${targetId}`, 'DELETE', null, function () {
                    alert('Bookmark deleted successfully.');
                    loadBookmarks();
                });
            }
        }
    });

    contextMenu.on('click', '#refresh-area', function () {
        const targetType = contextMenu.data('target-type');

        if (targetType === 'directory') {
            loadFolderTree();
        } else if (targetType === 'bookmark') {
            loadBookmarks();
        }
    });

    contextMenu.on('click', '#refresh-page', function () {
        location.reload();
    });
    
    /**
     * Load all bookmarks and display them in the #bookmarks container.
     */
    function loadBookmarks() {
        apiRequest('/api/bookmarks', 'GET', null, function (data) {
            $('#bookmarks').empty();
            if (!data || data.length === 0) {
                $('#bookmarks').append('<div class="placeholder">No bookmarks found.</div>');
            } else {
                data.forEach(function (bookmark) {
                    $('#bookmarks').append(`
                        <div class="bookmark-item">
                            <a href="${bookmark.url}" target="_blank">${bookmark.title}</a> - ${bookmark.description || 'No description'}
                            <button class="edit-bookmark" data-id="${bookmark.id}">Edit</button>
                            <button class="delete-bookmark" data-id="${bookmark.id}">Delete</button>
                        </div>
                    `);
                });
            }
        });
    }

    /**
     * Load the folder tree and display it in the #folder-tree container.
     */
    function loadFolderTree() {
        $.get('/api/directories', function (data) {
            $('#folder-tree').empty();
            if (!data || data.length === 0) {
                $('#folder-tree').append('<div class="placeholder">No folders available.</div>');
            } else {
                data.forEach(function (directory) {
                    $('#folder-tree').append(`
                        <div class="folder-item">${directory.name}</div>
                    `);
                });
            }
        }).fail(function () {
            $('#folder-tree').empty();
            $('#folder-tree').append('<div class="error">Error loading folder tree. Please try again later.</div>');
        });
    }

    /**
     * Load both bookmarks and folder tree.
     */
    function loadData() {
        loadBookmarks();
        loadFolderTree();
    }

    /**
     * Handle form submission for adding a new bookmark.
     */
    $('#details-form').submit(function (event) {
        event.preventDefault();
        const title = $('#details-title').val().trim();
        const url = $('#details-url').val().trim();
        const description = $('#details-description').val().trim();
        const tags = $('#details-tags').val().split(',').map(tag => tag.trim());
        const directory = $('#details-directory').val().trim();
    
        if (!title || !url) {
            alert('Please fill in both the Title and URL fields.');
            return;
        }
    
        $.ajax({
            url: '/api/bookmarks',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ title, url, description, tags, directory }),
            success: function () {
                loadBookmarks();
                $('#details-form')[0].reset(); // Clear the form after submission
            },
            error: function () {
                alert('Error adding bookmark. Please try again.');
            }
        });
    });

    // Listen for the "Enter" key press on the form
    $('#details-form').on('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default form submission behavior

            // Trigger form submission if Title and URL are filled
            const title = $('#details-title').val().trim();
            const url = $('#details-url').val().trim();

            if (title && url) {
                $(this).submit(); // Trigger the form submission
            } else {
                alert('Please fill in both the Title and URL fields before submitting.');
            }
        }
    });

    /**
     * Handle bookmark deletion.
     */
    $(document).on('click', '.delete-bookmark', function () {
        const id = $(this).data('id');
        apiRequest(`/api/bookmarks/${id}`, 'DELETE', null, function () {
            loadBookmarks();
        });
    });

    /**
     * Handle bookmark editing.
     */$(document).on('click', '.edit-bookmark', function () {
    const id = $(this).data('id');
    const title = prompt('Enter new title:');
    const url = prompt('Enter new URL:');
    const description = prompt('Enter new description:');
    const tags = prompt('Enter new tags (comma separated):').split(',').map(tag => tag.trim());
    const directory = prompt('Enter new directory:');

    if (title && url) {
        $.ajax({
            url: `/api/bookmarks/${id}`,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({ title, url, description, tags, directory }),
            success: function () {
                loadBookmarks();
            },
            error: function () {
                alert('Error updating bookmark. Please try again.');
            }
        });
    }
});

    /**
     * Handle downloading bookmarks as a text file.
     */
    $('#download-bookmarks').click(function () {
        $.get('/api/bookmarks', function (data) {
            if (!data || data.length === 0) {
                alert('No bookmarks available to download.');
                return;
            }

            let content = '';
            data.forEach(function (bookmark) {
                content += `${bookmark.title} - ${bookmark.url}\n`;
            });

            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'bookmarks.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }).fail(function () {
            alert('Error downloading bookmarks. Please try again.');
        });
    });

    // Toggle form visibility
    $('#toggle-form').click(function () {
        const formColumn = $('#form-column');
        if (formColumn.hasClass('collapsed')) {
            formColumn.removeClass('collapsed');
            $(this).text('Hide Form');
        } else {
            formColumn.addClass('collapsed');
            $(this).text('Show Form');
        }
    });

    // Load both bookmarks and folder tree on page load
    loadData();
});

function apiRequest(url, method, data = null, successCallback, errorCallback) {
    $.ajax({
        url: url,
        method: method,
        contentType: 'application/json',
        data: data ? JSON.stringify(data) : null,
        success: successCallback,
        error: errorCallback || function () {
            alert('An error occurred while processing your request.');
        }
    });
}