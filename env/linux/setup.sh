#!/bin/bash

# Create a virtual environment for Linux
python3 -m venv ../../env/linux/venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate the virtual environment
source ../../env/linux/venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip, setuptools, and wheel."
    exit 1
fi

# Install dependencies from requirements.txt
pip install -r ../../requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies from requirements.txt."
    exit 1
fi

echo "Setup completed successfully."