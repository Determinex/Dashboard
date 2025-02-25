@echo off
setlocal

REM Create a virtual environment for Windows
py -m venv ..\..\env\windows\venv
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

REM Activate the virtual environment
CALL ..\..\env\windows\venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

REM Upgrade pip, setuptools, and wheel
CALL python -m pip install --upgrade pip setuptools wheel
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to upgrade pip, setuptools, and wheel.
    pause
    exit /b %ERRORLEVEL%
)

REM Install dependencies from requirements.txt
CALL python -m pip install -r ..\..\requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies from requirements.txt.
    pause
    exit /b %ERRORLEVEL%
)

echo Setup completed successfully.
pause