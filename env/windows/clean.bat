@echo off
setlocal

REM Define the relative path to the database file
set DATABASE_FILE=..\..\database\dashboard.db

REM Remove virtual environment
IF EXIST ..\..\env\windows (
    rmdir /s /q ..\..\env\windows
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to delete virtual environment.
        pause
        exit /b %ERRORLEVEL%
    )
    echo Virtual environment deleted successfully.
) ELSE (
    echo No virtual environment found.
)

REM Remove database file
IF EXIST %DATABASE_FILE% (
    del /q %DATABASE_FILE%
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to delete database file.
        pause
        exit /b %ERRORLEVEL%
    )
    echo Database file deleted successfully.
) ELSE (
    echo No database file found.
)

pause