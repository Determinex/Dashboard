document.addEventListener('DOMContentLoaded', function() {

  /*******************************************************************
   * Bookmark Manager Object
   *******************************************************************/

  const BookmarkManager = (() => {
    // Private Data
    let directories = [
      {
        id: "11111111-1111-4111-b111-111111111111",
        name: "Root",
        isOpen: true,
        bookmarks: [],
        children: [
          {
            id: "22222222-2222-4222-b222-222222222222",
            name: "Personal",
            isOpen: false,
            bookmarks: ["d0d6277d-7d7d-7d7d-d7d7-7d7d7d7d7d7d"],
            children: [
              {
                id: "44444444-4444-4444-b444-444444444444",
                name: "Programming",
                isOpen: false,
                bookmarks: ["a7a3944a-4a4a-4a4a-a4a4-4a4a4a4a4a4a"],
                children: [
                  {
                    id: "66666666-6666-4666-b666-666666666666",
                    name: "JavaScript",
                    isOpen: false,
                    bookmarks: [],
                    children: []
                  },
                  {
                    id: "77777777-7777-4777-b777-777777777777",
                    name: "HTML",
                    isOpen: false,
                    bookmarks: [],
                    children: []
                  },
                  {
                    id: "88888888-8888-4888-b888-888888888888",
                    name: "CSS",
                    isOpen: false,
                    bookmarks: [],
                    children: []
                  },
                  {
                    id: "99999999-9999-4999-b999-999999999999",
                    name: "Python",
                    isOpen: false,
                    bookmarks: [],
                    children: []
                  },
                ]
              },
              {
                id: "00000000-0000-4000-b000-000000000000",
                name: "PC",
                isOpen: false,
                bookmarks: ["e1e7388e-8e8e-8e8e-e8e8-8e8e8e8e8e8e", "f2f8499f-9f9f-9f9f-f9f9-9f9f9f9f9f9f", "03095a00-0a0a-0a0a-0a0a-0a0a0a0a0a0a"],
                children: []
              }
            ]
          },
          {
            id: "33333333-33e3-4333-b333-3333g3333333",
            name: "Professional",
            isOpen: false,
            bookmarks: ["b8b4055b-5b5b-5b5b-b5b5-5b5b5b5b5b5b", "c9c5166c-6c6c-6c6c-c6c6-6c6c6c6c6c6c"],
            children: [
              {
                id: "33e33333-3333-4333-b333-333333g33333",
                name: "Work",
                isOpen: false,
                bookmarks: [],
                children: []
              },
              {
                id: "33333333-3033-43e3-b333-3333333333g3",
                name: "Projects",
                isOpen: false,
                bookmarks: [],
                children: []
              }
            ]
          }
        ]
      }
    ];
    let bookmarks = [
      {
        id: "a7a3944a-4a4a-4a4a-a4a4-4a4a4a4a4a4a",
        url: "https://www.example.com/very-long-url-path-that-could-cause-overflow-or-breaks",
        name: "Example Site | A Long Name",
        description: "This is an example bookmark with a somewhat longer description than usual. It has enough text to demonstrate truncation and expansion on click. It also tests wrapping long words and URLs.",
        isFavorite: false,
        tags: ["example", "extended"]
      },
      {
        id: "b8b4055b-5b5b-5b5b-b5b5-5b5b5b5b5b5b",
        url: "https://www.mozilla.org",
        name: "Mozilla",
        description: "Firefox browser homepage.",
        isFavorite: true,
        tags: ["Mozilla", "MDN"],
      },
      {
        id: "c9c5166c-6c6c-6c6c-c6c6-6c6c6c6c6c6c",
        url: "https://www.wikipedia.org",
        name: "Wikipedia",
        description: "Free online encyclopedia.",
        isFavorite: false,
        tags: ["Wiki"]
      },
      {
        id: "d0d6277d-7d7d-7d7d-d7d7-7d7d7d7d7d7d",
        url: "https://us.ecoflow.com/products/delta-pro-ultra?variant=54357493088329",
        name: "EcoFlow | Home System",
        description: "EcoFlow DELTA Pro Ultra Whole-Home Backup Power (UL 9540 Certificated)",
        isFavorite: false,
        tags: ["EcoFlow", "Solar"]
      },
      {
        id: "e1e7388e-8e8e-8e8e-e8e8-8e8e8e8e8e8e",
        url: "https://a.co/d/8C1kCYL",
        name: "Gen 5 Mobo",
        description: "Micro Center AMD Ryzen 9 9950X CPU Processor with MSI MAG X870E Tomahawk WiFi ATX Motherboard (DDR5, PCIe 5.0 x16, M.2 Gen5, Wi-Fi 7, 5G LAN)",
        isFavorite: false,
        tags: ["PC", "Motherboard"]
      },
      {
        id: "f2f8499f-9f9f-9f9f-f9f9-9f9f9f9f9f9f",
        url: "https://a.co/d/4ov0UYd",
        name: "Gen 5 GPU",
        description: "MSI GeForce RTX 5090 32G Gaming Trio OC 32GB GDDR7 (28Gbps/512-bit), PCIe 5, Boost: 2482MHz, HDMI 2.1b, DisplayPort 2.1b",
        isFavorite: false,
        tags: ["PC", "Graphics Card"]
      },
      {
        id: "03095a00-0a0a-0a0a-0a0a-0a0a0a0a0a0a",
        url: "https://us.msi.com/Laptop/Titan-18-HX-Dragon-Edition-Norse-Myth-A2XWX/shopnow",
        name: "MSI Titan Laptop",
        description: 'MSI Titan 18 HX Dragon Edition Norse Myth A2XWJG-440US - 18" UHD+ 120Hz Mini LED - Ultra 9-285HX - RTX 5090',
        isFavorite: false,
        tags: ["PC", "MSI"]
      }
    ];

    // DOM elements
    const domElements = {
      directoryStructure: document.getElementById('directory-structure'),
      bookmarkTableBody: document.getElementById('bookmark-table-body')
    };
    // Private Methods
    /*******************************************************************
     * Rendering Functions
     *******************************************************************/

    function renderdirectories(tree, parentElement) {
      console.log("renderdirectories() called", tree, parentElement);

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
          renderdirectories(node.children, ul); // Recursive call
          li.appendChild(ul);
        }

        // Add click event to toggle the collapsed state and display bookmarks
        li.addEventListener('click', (event) => {
          event.stopPropagation(); // Prevent event from bubbling up
          li.classList.toggle('collapsed'); // Toggle the collapsed class
          li.classList.toggle('expanded'); // Toggle the expanded class

          // Clear the bookmarks table
          domElements.bookmarkTableBody.innerHTML = ''; // Clear existing content

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

    function renderBookmarks(displayBookmarks) {
      console.log("renderBookmarks() called", displayBookmarks);
      const DESCRIPTION_LIMIT = 40; // Character limit for description truncation
      console.log("DESCRIPTION_LIMIT:", DESCRIPTION_LIMIT);
      domElements.bookmarkTableBody.innerHTML = '';
      console.log("bookmarkTableBody:", domElements.bookmarkTableBody);

      function createStarSVG() {
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("class", "star-svg");
        svg.setAttribute("viewBox", "0 0 24 24");
        svg.setAttribute("aria-hidden", "true");
        svg.setAttribute("focusable", "false");

        const polygon = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        polygon.setAttribute("points", "12 2 15 9 22 9 17 14 19 21 12 17 5 21 7 14 2 9 9 9");

        svg.appendChild(polygon);
        return svg;
      }

      displayBookmarks.forEach(bookmark => {
        const tr = document.createElement('tr');
        tr.dataset.id = bookmark.id;
        tr.setAttribute('draggable', 'true');

        tr.addEventListener('click', (event) => {
          event.stopPropagation();

          // Deselect other bookmarks
          document.querySelectorAll('#bookmark-table-body tr.selected').forEach(el => {
            el.classList.remove('selected');
          });

          // Select this bookmark
          tr.classList.add('selected');
        });

        const favoriteTd = document.createElement('td');
        favoriteTd.classList.add('favorite-col');
        const starButton = document.createElement('button');
        starButton.classList.add('star-button');
        if (bookmark.isFavorite) {
          starButton.classList.add('active');
        }
        starButton.setAttribute('aria-label', bookmark.isFavorite ? 'Unmark as favorite' : 'Mark as favorite');

        starButton.appendChild(createStarSVG());

        starButton.addEventListener('click', () => {
          bookmark.isFavorite = !bookmark.isFavorite;
          starButton.classList.toggle('active');
          starButton.setAttribute('aria-label', bookmark.isFavorite ? 'Unmark as favorite' : 'Mark as favorite');

          starButton.innerHTML = '';
          starButton.appendChild(createStarSVG());
        });

        favoriteTd.appendChild(starButton);
        tr.appendChild(favoriteTd);

        const siteTd = document.createElement('td');
        siteTd.classList.add('site-col');
        const anchor = document.createElement('a');
        anchor.href = bookmark.url;
        anchor.target = "_blank";
        anchor.rel = "noopener noreferrer";
        anchor.textContent = bookmark.name;
        siteTd.appendChild(anchor);
        tr.appendChild(siteTd);

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
          toggleSpan.textContent = "  ...";

          toggleSpan.addEventListener('click', () => {
            const isExpanded = tr.classList.toggle('expanded');
            if (isExpanded) {
              descSpan.textContent = fullDesc;
              descSpan.classList.remove('desc-truncated');
              toggleSpan.textContent = " \u21A9";
            } else {
              descSpan.textContent = truncatedText;
              descSpan.classList.add('desc-truncated');
              toggleSpan.textContent = " ...";
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

        const tagsTd = document.createElement('td');
        tagsTd.classList.add('tags-col');
        const tagsSpan = document.createElement('span');
        tagsSpan.textContent = bookmark.tags.join(', ');
        tagsTd.appendChild(tagsSpan);
        tr.appendChild(tagsTd);

        domElements.bookmarkTableBody.appendChild(tr);
      });
    }

    /*******************************************************************
     * UI Update Functions
     *******************************************************************/

    function updateUI() {
      console.log("updateUI() called");
      displayDirectoryStructure();
      initializeBookmarkTable();
    }

    function displayDirectoryStructure() {
      console.log("displayDirectoryStructure() called");
      console.log("directoryStructureElement:", domElements.directoryStructure);
      domElements.directoryStructure.innerHTML = '';
      renderdirectories(directories, domElements.directoryStructure);
    }

    function initializeBookmarkTable() {
      console.log("initializeBookmarkTable() called");
      console.log("tbody:", domElements.bookmarkTableBody);
      domElements.bookmarkTableBody.innerHTML = '';
      const rootDirectory = directories[0];

      const displayBookmarks = bookmarks.filter(b => rootDirectory.bookmarks && rootDirectory.bookmarks.includes(b.id));

      if (displayBookmarks.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.classList.add('default-table-message')
        td.colSpan = 4;
        td.innerHTML = 'If this is your first time using this application:<br>Check out the options in the menu.<br><br><u>Bookmarks will be displayed here.</u><br>To see your bookmarks,<br>please navigate through the directories to the left.';
        tr.appendChild(td);
        domElements.bookmarkTableBody.appendChild(tr);
      } else {
        renderBookmarks(displayBookmarks);
      }
    }

    function getCurrentDirectory() {
      const activeLi = document.querySelector('#directory-structure li.expanded');
      if (!activeLi) return directories[0];
      return directories.find(node => node.id === activeLi.dataset.id);
    }
  
  /*******************************************************************
     * Initialization
     *******************************************************************/

    // Call the updateUI function to initialize the UI
    updateUI();

    /*******************************************************************
     * Public Interface
     *******************************************************************/

    return {
      // Expose any functions or data that you want to be accessible from outside
    };
  })(); // End of BookmarkManager IIFE

  /*******************************************************************
   * Initialization
   *******************************************************************/
  // Wait for the DOM to be fully loaded before initializing the BookmarkManager
  console.log("DOMContentLoaded event fired");
  console.log("Initializing BookmarkManager...");
  // Initialize the BookmarkManager
  // BookmarkManager.initialize();
    
  
  // You can call functions from the BookmarkManager here if needed
  // BookmarkManager.somePublicFunction();
  console.log("BookmarkManager initialized");
});