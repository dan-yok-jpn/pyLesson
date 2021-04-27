
: Set up the environment for Visual Studio Code

@echo off
setlocal

if "%PYTHONHOME%"=="" (call setenv)

if %ERRORLEVEL%==1 (
    echo.
    echo ^ Cannot set up because there is no suitable Python
    exit
)

set dst=%APPDATA%\Code\User

python mkSettings.py %PYTHONHOME% > %dst%\settings.json
