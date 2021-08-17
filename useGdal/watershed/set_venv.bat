@echo off

set OSGEO_ROOT=C:\OSGeo4W
set PYTHON=%OSGEO_ROOT%\apps\Python39\python.exe

mkdir .vscode
call :genJSON_1 > .vscode\settings.json
call :genJSON_2 > .vscode\launch.json
call :genBat    > tmp.bat
powershell Start-Process tmp.bat -Verb runas -Wait
del tmp.bat
call .venv\Scripts\activate.bat
pip install -r requirements.txt
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
    echo %PYTHON% -m venv --system-site-packages --upgrade-deps .venv
    echo call :genPython ^> .venv\Lib\site-packages\gdal_env.py
	echo goto :eof
    echo :genPython
    echo     echo import os
    echo     echo class gdal_env:
    echo     echo     def __init__(self):
    echo     echo         OSGEO_ROOT = '%OSGEO_ROOT%'.replace('\\', '\\')
    echo     echo         OSGEO_BIN  = OSGEO_ROOT + '\\bin'
    echo     echo         os.environ['PATH']             = OSGEO_BIN  + ';' + os.environ['PATH']
    echo     echo         os.environ['GDAL_DATA']        = OSGEO_ROOT + '\\share\\gdal'
    echo     echo         os.environ['GDAL_DRIVER_PATH'] = OSGEO_BIN  + '\\gdalplugins'
    echo     echo         os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + '\\share\\epsg_csv'
    echo     echo         os.environ['PROJ_LIB']         = OSGEO_ROOT + '\\share\\proj'
    echo     echo         os.add_dll_directory(OSGEO_BIN)
    echo     echo         self.OSGEO_ROOT = OSGEO_ROOT
    echo     exit /b
    exit /b
