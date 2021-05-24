@echo off

set EXE=C:\OSGeo4W64\apps\Python37\python.exe

mkdir .vscode
call :genJSON_1 > .vscode\settings.json
call :genJSON_2 > .vscode\launch.json
call :genBat    > tmp.bat
powershell Start-Process tmp.bat -Verb runas
goto :eof

:genJSON_1
    echo {
    echo     "files.eol": "\n",
    echo     "terminal.integrated.env.windows": {
    echo         "PATH": "${workspaceRoot}\\.venv\\Scripts;${env:PATH}"
    echo     },
    echo     "python.pythonPath": "${workspaceRoot}\\.venv\\Scripts\\Python.exe"
    echo }
    exit /b
    
:genJSON_2:
    echo {
    echo     "version": "0.2.0",
    echo     "configurations": [
    echo         {
    echo             "name": "Python: Current File",
    echo             "type": "python",
    echo             "request": "launch",
    echo             "program": "${file}",
    echo             "console": "integratedTerminal"
    echo         }
    echo     ]
    echo }
    exit /b

:genBat
    echo cd "%~dp0"
    echo %EXE% -m venv --system-site-packages --symlinks --without-pip --clear .venv
    echo del tmp.bat
    exit /b