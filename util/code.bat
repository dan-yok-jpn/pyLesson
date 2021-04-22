@echo off
setlocal
set VSCODE_DEV=
set ELECTRON_RUN_AS_NODE=1

set root=%LOCALAPPDATA%\\Programs\Micros~1
:       =C:\Users\nkmanager\AppData\Local\Programs\Microsoft VS Code

%root%\Code.exe %root%\resources\app\out\cli.js %*
endlocal
