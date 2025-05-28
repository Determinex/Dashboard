// This file is part of the Bookmark Manager plugin for a web application.
// Bookmark Manager for organizing and managing bookmarks.
// This code provides a basic structure for a bookmark manager, including directory management, bookmark rendering, and UI updates.

// Bookmark Manager JavaScript Code

// Function to get the next available directory ID
function getNextDirectoryId() {
    return directoryTree.length > 0 ? Math.max(...directoryTree.map(d => d.id)) + 1 : 1;
}

// Function to get the next available bookmark ID
function getNextBookmarkId() {
    return bookmarks.length > 0 ? Math.max(...bookmarks.map(b => b.id)) + 1 : 1;
}

// Example directory structure with bookmarks
const directoryTree = [
    {
        id: 1,
        name: "Root",
        isOpen: true,
        bookmarks: [],
        children: [
            {
                id: 2,
                name: "Personal",
                isOpen: false,
                bookmarks: [],
                children: [
                    {
                        id: 4,
                        name: "Programming",
                        isOpen: false,
                        bookmarks: [1], // Reference to bookmark IDs
                        children: []
                    }
                ]
            },
            {
                id: 3,
                name: "Professional",
                isOpen: false,
                bookmarks: [2, 3], // Reference to bookmark IDs
                children: []
            }
        ]
    }
];

// Example bookmark data fetched from database
const bookmarks = [
    {
        id: 1,
        url: "https://www.example.com/very-long-url-path-that-could-cause-overflow-or-breaks",
        name: "Example Site | A Long Name",
        description: "This is an example bookmark with a somewhat longer description than usual. It has enough text to demonstrate truncation and expansion on click. It also tests wrapping long words and URLs.",
        isFavorite: false,
        tags: ["example", "extended"]
    },
    {
        id: 2,
        url: "https://www.mozilla.org",
        name: "Mozilla",
        description: "Firefox browser homepage.",
        isFavorite: true,
        tags: ["Mozilla", "MDN"],
    },
    {
        id: 3,
        url: "https://www.wikipedia.org",
        name: "Wikipedia",
        description: "Free online encyclopedia.",
        isFavorite: false,
        tags: ["Wiki"]
    }
];



function renderDirectoryTree(tree, parentElement) {
    tree.forEach(node => {
        const li = document.createElement('li');

        // Check the isOpen property to determine the initial class
        if (node.isOpen) {
            li.classList.add('expanded'); // Add 'expanded' class if isOpen is true
        } else {
            li.classList.add('collapsed'); // Add 'collapsed' class if isOpen is false
        }

        li.textContent = node.name;

        // If the node has children, create a nested ul
        if (node.children && node.children.length > 0) {
            const ul = document.createElement('ul');
            renderDirectoryTree(node.children, ul); // Recursive call
            li.appendChild(ul);
        }

        // Add click event to toggle the collapsed state and display bookmarks
        li.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent event from bubbling up
            li.classList.toggle('collapsed'); // Toggle the collapsed class

            // Clear the bookmarks table
            const tbody = document.getElementById('bookmark-table-body');
            tbody.innerHTML = ''; // Clear existing content

            // Check if the clicked directory has bookmarks
            if (node.bookmarks) {
                const bookmarksToDisplay = bookmarks.filter(b => node.bookmarks.includes(b.id));
                if (bookmarksToDisplay.length > 0) {
                    renderBookmarks(bookmarksToDisplay); // Render bookmarks if available
                } else {
                    // If no bookmarks, show the initialized message
                    initializeBookmarkTable();
                }
            } else {
                // If no bookmarks, show the initialized message
                initializeBookmarkTable();
            }
        });

        parentElement.appendChild(li);
    });
}

function renderBookmarks(bookmarksToDisplay) {
    const tbody = document.getElementById('bookmark-table-body');
    tbody.innerHTML = ''; // Clear existing content

    bookmarksToDisplay.forEach(bookmark => {
        const DESCRIPTION_LIMIT = 35; // max characters before truncation
        const starSVG = `
        <svg class="star-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false" >
        <polygon points="12 2 15 9 22 9 17 14 19 21 12 17 5 21 7 14 2 9 9 9"></polygon>
        </svg>
        `; // SVG for bookmark 'favorites' star icon
        const tr = document.createElement('tr');

        // Favorite star button cell
        const favoriteTd = document.createElement('td');
                favoriteTd.classList.add('favorite-col');
        const starButton = document.createElement('button');
        starButton.classList.add('star-button');
        if (bookmark.isFavorite) {
            starButton.classList.add('active');
        }
        starButton.setAttribute('aria-label', bookmark.isFavorite ? 'Unmark as favorite' : 'Mark as favorite');
        starButton.innerHTML = starSVG;
        starButton.addEventListener('click', () => {
            bookmark.isFavorite = !bookmark.isFavorite;
            starButton.classList.toggle('active');
            starButton.setAttribute('aria-label', bookmark.isFavorite ? 'Unmark as favorite' : 'Mark as favorite');
        });
        favoriteTd.appendChild(starButton);
        tr.appendChild(favoriteTd);

        // Site cell
        const siteTd = document.createElement('td');
        siteTd.classList.add('site-col');
        const anchor = document.createElement('a');
        anchor.href = bookmark.url;
        anchor.target = "_blank";
        anchor.rel = "noopener noreferrer";
        anchor.textContent = bookmark.name;
        siteTd.appendChild(anchor);
        tr.appendChild(siteTd);

        // Description cell with truncation and expand
        const descTd = document.createElement('td');
        descTd.classList.add('desc-col');

        const fullDesc = bookmark.description;
        if (fullDesc.length > DESCRIPTION_LIMIT) {
            const truncatedText = fullDesc.slice(0, DESCRIPTION_LIMIT - 3);
            const descSpan = document.createElement('span');
            descSpan.classList.add('desc-text', 'desc-truncated');
            descSpan.textContent = truncatedText;

            const toggleSpan = document.createElement('span');
            toggleSpan.classList.add('desc-expand-toggle');
            toggleSpan.textContent = "...";

            toggleSpan.addEventListener('click', () => {
                const isExpanded = tr.classList.toggle('expanded');
                if (isExpanded) {
                    descSpan.textContent = fullDesc;
                    descSpan.classList.remove('desc-truncated');
                    toggleSpan.textContent = "↩";
                } else {
                    descSpan.textContent = truncatedText;
                    descSpan.classList.add('desc-truncated');
                    toggleSpan.textContent = "...";
                }
            });

            descTd.appendChild(descSpan);
            descTd.appendChild(toggleSpan);
        } else {
            const descSpan = document.createElement('span');
            descSpan.classList.add('desc-text');
            descSpan.textContent = fullDesc;
            descTd.appendChild(descSpan);
        }
        tr.appendChild(descTd);
        
        // Tags cell
        const tagsTd = document.createElement('td');
        tagsTd.classList.add('tags-col');
        const tagsSpan = document.createElement('span');
        tagsSpan.textContent = bookmark.tags.join(', ');
        tagsTd.appendChild(tagsSpan);
        tr.appendChild(tagsTd);

        tbody.appendChild(tr);
    });
}

function updateUI() {
    displayDirectoryStructure();
    initializeBookmarkTable();
}

function displayDirectoryStructure() {
    const directoryStructureElement = document.getElementById('directory-structure');
    directoryStructureElement.innerHTML = ''; // Clear existing content
    renderDirectoryTree(directoryTree, directoryStructureElement);
}

function initializeBookmarkTable() {
    const tbody = document.getElementById('bookmark-table-body');
    const rootDirectory = directoryTree[0]; // Assuming the first item is the root

    // Check if there are bookmarks associated with the root directory
    const bookmarksToDisplay = bookmarks.filter(b => rootDirectory.bookmarks && rootDirectory.bookmarks.includes(b.id));

    if (bookmarksToDisplay.length === 0) {
        // Create a new row and cell for the message
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 4; // Span across all columns
        td.textContent = "Bookmarks will be displayed here. To see your bookmarks, please navigate through the directory tree above.";
        td.style.textAlign = "center"; // Center the text
        tr.appendChild(td);
        tbody.appendChild(tr);
    } else {
        // If there are bookmarks, render them
        renderBookmarks(bookmarksToDisplay);
    }
}

// Call the updateUI function to initialize the UI
updateUI();