:: batch filename: start_servers.bat
:: For running in Powershell from the same directory:
:: Start-Process cmd.exe "/c cd `"$PWD`" & .\start_servers.bat" -verb RunAs

@echo off
:: Change directory to the location of the Flask server (relative path)
cd /d ".\flask_server"

:: Set the FLASK_APP environment variable and start the Flask server
set FLASK_APP=app.py
start cmd /k "flask run"

if  errorlevel 1 goto ERROR
echo SUCCESSFUL

:: Change directory to the location of the Node.js server (relative path)
cd /d ".\node_server"

:: Start the Node.js server in a new command window
start cmd /k "node server.js"

echo Both servers are starting...
pause

if  errorlevel 1 goto ERROR
echo SUCCESSFUL
goto EOF 

:ERROR
echo Failed
cmd /k
exit /b 1

:EOF 
