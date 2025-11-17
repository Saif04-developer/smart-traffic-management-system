#!/bin/bash
# Smart Traffic Management - Run Script for macOS/Linux

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Set Flask environment variables
export FLASK_APP=app.main
export FLASK_ENV=development

# Run Flask
echo "Starting Flask development server..."
flask run --reload
