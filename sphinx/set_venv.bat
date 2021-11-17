@echo off
setlocal

set PYTHONHOME=C:\Progra~2\micros~4\shared\Python37_64
set PATH=%PYTHONHOME%;%PYTHONHOME%\DLLs;%PYTHONHOME%\Scripts;%PATH%

if not exist %PYTHONHOME% (
    echo.
    echo    ERROR !   %PYTHONHOME% not found.
    echo    Check this Scripts
    echo.
    goto :eof
)

if not exist .vscode (mkdir .vscode)
call :genJSON_1 > .vscode\settings.json
call :genJSON_2 > .vscode\launch.json
call :genBat    > tmp.bat
powershell Start-Process tmp.bat -Verb runas -Wait
del tmp.bat
pip install -r requirements.txt -t .venv\Lib\site-packages 1>nul 2>nul
goto :eof

:genJSON_1
    echo {
    echo     "terminal.integrated.automationShell.windows": "C:\\WINDOWS\\System32\\cmd.exe",
    echo     "terminal.integrated.defaultProfile.windows": "Command Prompt",
    echo     "python.envFile": "${workspaceFolder}\\.venv",
    echo     "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe"
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
    echo @echo off
    echo cd "%~dp0"
    echo "%PYTHONHOME%\python" -m venv --system-site-packages --symlinks --without-pip --clear .venv
   exit /b
