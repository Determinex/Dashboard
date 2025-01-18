const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware to log requests
app.use((req, res, next) => {
    console.log(`Request received: ${req.method} ${req.url}`);
    next();
});

// Function to recursively scan directories
function scanDirectory(dir) {
    let results = [];
    const list = fs.readdirSync(dir); // Read directory contents
    list.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat && stat.isDirectory()) {
            // If it's a directory, recurse into it
            results.push({
                name: file,
                path: filePath,
                type: 'directory',
                children: scanDirectory(filePath) // Recursively scan subdirectory
            });
        } else {
            // If it's a file, add to results
            results.push({
                name: file,
                path: filePath,
                type: 'file'
            });
        }
    });
    return results;
}

// Define API endpoint to get directory structure
app.get('/api/directory', (req, res) => {
    const baseDirectory = path.join(__dirname, '../'); // Change this to your desired base path
    const directoryStructure = scanDirectory(baseDirectory);
    res.json(directoryStructure); // Send directory structure as JSON
});

// Start the server
app.listen(PORT, '127.0.0.1', () => {
    console.log(`Node.js server is running on http://127.0.0.1:${PORT}`);
});