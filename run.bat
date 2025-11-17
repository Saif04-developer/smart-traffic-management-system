@echo off
REM Smart Traffic Management - Run Script for Windows

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM Set Flask environment variables
set FLASK_APP=app.main
set FLASK_ENV=development

REM Run Flask
echo Starting Flask development server...
flask run --reload
