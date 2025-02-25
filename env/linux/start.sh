#!/bin/bash

# Set the working directory to the script's location
cd "$(dirname "$0")" || exit

# Activate the virtual environment
source ../../env/linux/venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Set environment variables for Flask
export FLASK_APP=app.py
export FLASK_ENV=development

# Start the Flask server
flask run --debug
if [ $? -ne 0 ]; then
    echo "Failed to start Flask server."
    exit 1
fi

# Keep the terminal open (optional)
exec bash