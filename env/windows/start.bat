@echo off
REM Set the working directory to the script's location
setlocal

REM Change to the script's directory
cd /d "%~dp0"

REM Activate the virtual environment
CALL venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

REM Set environment variables for Flask
set FLASK_APP=src/app.py
set FLASK_ENV=development

REM Start the Flask server
CALL flask run --debug
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to start Flask server.
    pause
    exit /b %ERRORLEVEL%
)

pause