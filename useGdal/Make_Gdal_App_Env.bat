@echo off

set OSGEO_ROOT=C:\OSGeo4W64
set EXE=%OSGEO_ROOT%\apps\Python37\python.exe

mkdir .vscode
call :genJSON_1 > .vscode\settings.json
call :genJSON_2 > .vscode\launch.json
call :genBat    > tmp.bat
powershell Start-Process tmp.bat -Verb runas
: del tmp.bat
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
    echo @echo off
    echo cd "%~dp0"
    echo %EXE% -m venv --system-site-packages --symlinks --without-pip --clear .venv
    echo call :genPython ^> .venv\Lib\site-packages\gdal_env.py
	echo goto :eof
    echo :genPython
    echo     echo import os
    echo     echo import sys
    echo     echo class gdal_env:
    echo     echo     def __init__(self):
    echo     echo         OSGEO_ROOT = '%OSGEO_ROOT%'.replace('\\', '\\')
    echo     echo         os.environ['PATH']             = OSGEO_ROOT + '\\bin;' + os.environ['PATH']
    echo     echo         os.environ['GDAL_DATA']        = OSGEO_ROOT + '\\share\\gdal'
    echo     echo         os.environ['GDAL_DRIVER_PATH'] = OSGEO_ROOT + '\\bin\\gdalplugins'
    echo     echo         os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + '\\share\\epsg_csv'
    echo     echo         os.environ['PROJ_LIB']         = OSGEO_ROOT + '\\share\\proj'
    echo     echo         self.OSGEO_ROOT = OSGEO_ROOT
    echo     exit /b
    exit /b
