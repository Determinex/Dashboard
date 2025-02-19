$(document).ready(function(){
    // Tab switching functionality
    $('.tablink').click(function(){
        var tab_id = $(this).attr('data-tab');

        $('.tablink').removeClass('active');
        $('.tab-pane').removeClass('active');

        $(this).addClass('active');
        $("#"+tab_id).addClass('active');
    });

    // Initialize tooltip
    $('.wow-tooltip').tooltipster({
        content: $(this).data('tooltip-content'),
        theme: 'tooltipster-light',
        animation: 'fade',
        delay: 200,
        position: 'top'
    });

    // Search functionality
    $('#search-input').on('keyup', function() {
        var searchQuery = $(this).val();
        $.ajax({
            type: 'POST',
            url: '/search-notes',
            data: JSON.stringify({query: searchQuery}),
            contentType: 'application/json',
            success: function(data) {
                var notesHtml = '';
                $.each(data, function(index, note) {
                    notesHtml += '<div class="note-card" data-id="' + note.id + '">' + note.title + '</div>';
                });
                $('#notes-list').html(notesHtml);
            }
        });
    });

    // Drag and drop functionality
    var el = document.getElementById('notes-list');
    var sortable = Sortable.create(el, {
        animation: 150,
        onSort: function(event) {
            var notes = [];
            $('.note-card').each(function(index, note) {
                notes.push($(note).data('id'));
            });
            $.ajax({
                type: 'POST',
                url: '/update-notes-order',
                data: JSON.stringify(notes),
                contentType: 'application/json',
                success: function(data) {
                    console.log(data);
                }
            });
        }
    });

    // Pin note functionality
    $(document).on('click', '.pin-button', function() {
        var noteId = $(this).data('id');
        $.ajax({
            type: 'POST',
            url: '/pin-note',
            data: JSON.stringify({id: noteId}),
            contentType: 'application/json',
            success: function(data) {
                // Move the pinned note to the pinned section
                var pinnedNote = $('.note-card[data-id="' + noteId + '"]').clone();
                $('#pinned-notes-list').append(pinnedNote);
                $('.note-card[data-id="' + noteId + '"]').remove(); // Remove from main list
            }
        });
    });

    // Initialize μPad editors
    var mupad1 = new MuPad('#editor-1', {
        theme: 'snow',
        modules: {
            toolbar: [
                ['bold', 'italic', 'underline'],        // toggled buttons
                ['link', 'image'],                       // link and image
                [{ 'list': 'ordered'}, { 'list': 'bullet' }] // lists
            ]
        }
    });

    var mupad2 = new MuPad('#editor-2', {
        theme: 'snow',
        modules: {
            toolbar: [
                ['bold', 'italic', 'underline'],        // toggled buttons
                ['link', 'image'],                       // link and image
                [{ 'list': 'ordered'}, { 'list': 'bullet' }] // lists
            ]
        }
    });

    // Tagging functionality
    $('#add-tag-button').on('click', function() {
        var tag = $('#tag-input').val();
        // Add tag to the note and update the database
        console.log("Tag added: " + tag);
        $('#tag-input').val(''); // Clear input
    });

    // Notebook management functionality
    $('#new-notebook-button').on('click', function() {
        var notebookName = prompt("Enter the name of the new notebook:");
        if (notebookName) {
            // Send AJAX request to create a new notebook
            $.ajax({
                type: 'POST',
                url: '/create-notebook',
                data: JSON.stringify({name: notebookName}),
                contentType: 'application/json',
                success: function(data) {
                    $('#notebook-list').append('<a href="#" class="notebook" data-id="' + data.id + '">' + notebookName + '</a>');
                }
            });
        }
    });

    $('#rename-notebook-button').on('click', function() {
        var selectedNotebook = $('.notebook.selected'); // Assuming you have a way to select a notebook
        if (selectedNotebook.length) {
            var newName = prompt("Enter the new name for the notebook:", selectedNotebook.text());
            if (newName) {
                // Send AJAX request to rename the notebook
                $.ajax({
                    type: 'POST',
                    url: '/rename-notebook',
                    data: JSON.stringify({id: selectedNotebook.data('id'), name: newName}),
                    contentType: 'application/json',
                    success: function(data) {
                        selectedNotebook.text(newName);
                    }
                });
            }
        } else {
            alert("Please select a notebook to rename.");
        }
    });

    $('#delete-notebook-button').on('click', function() {
        var selectedNotebook = $('.notebook.selected'); // Assuming you have a way to select a notebook
        if (selectedNotebook.length) {
            // Send AJAX request to delete the notebook
            $.ajax({
                type: 'POST',
                url: '/delete-notebook',
                data: JSON.stringify({id: selectedNotebook.data('id')}),
                contentType: 'application/json',
                success: function(data) {
                    selectedNotebook.remove();
                }
            });
        } else {
            alert("Please select a notebook to delete.");
        }
    });

    // User settings functionality
    $('#user-settings-button').on('click', function() {
        $('#userSettingsModal').modal('show');
    });

    $('#save-settings-button').on('click', function() {
        var selectedTheme = $('#theme-select').val();
        var selectedFontSize = $('#font-size-select').val();
        var selectedLineSpacing = $('#line-spacing-select').val();
        var noteBackgroundColor = $('#note-background-color').val();
        // Save user preferences (send to server if needed)
        console.log("User preferences saved: Theme - " + selectedTheme + ", Font Size - " + selectedFontSize + ", Line Spacing - " + selectedLineSpacing + ", Note Background Color - " + noteBackgroundColor);
        $('#userSettingsModal').modal('hide');
    });

    // Show/Hide toolbars based on state
    function showNoteToolbar() {
        $('#note-toolbar').show();
        $('#notebook-toolbar').hide();
    }

    function showNotebookToolbar() {
        $('#note-toolbar').hide();
        $('#notebook-toolbar').show();
    }

    function hideAllToolbars() {
        $('#note-toolbar').hide();
        $('#notebook-toolbar').hide();
    }

    // Example event handlers to show/hide toolbars
    $('.notebook').on('click', function() {
        showNotebookToolbar();
        // Load notebook contents and display in main content area
    });

    $('.note-card').on('click', function() {
        showNoteToolbar();
        // Load note contents and display in main content area
    });

    // Initially hide all toolbars
    hideAllToolbars();
});