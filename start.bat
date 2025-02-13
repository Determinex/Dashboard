@echo off
setlocal

CALL env\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

set FLASK_APP=src/app.py
set FLASK_ENV=development
CALL env\Scripts\flask run --debug
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to start Flask server.
    pause
    exit /b %ERRORLEVEL%
)

cmd /k