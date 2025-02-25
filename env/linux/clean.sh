#!/bin/bash

# Define the relative path to the database file
DATABASE_FILE="../../database/dashboard.db"

# Remove virtual environment
if [ -d "../../env/linux" ]; then
    rm -rf "../../env/windows"
    if [ $? -ne 0 ]; then
        echo "Failed to delete virtual environment."
        exit 1
    fi
    echo "Virtual environment deleted successfully."
else
    echo "No virtual environment found."
fi

# Remove database file
if [ -f "$DATABASE_FILE" ]; then
    rm -f "$DATABASE_FILE"
    if [ $? -ne 0 ]; then
        echo "Failed to delete database file."
        exit 1
    fi
    echo "Database file deleted successfully."
else
    echo "No database file found."
fi