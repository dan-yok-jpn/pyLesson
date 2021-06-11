@echo off
cd "C:\Users\nkmanager\Desktop\pyLesson\useGdal\"
C:\OSGeo4W64\apps\Python37\python.exe -m venv --system-site-packages --symlinks --without-pip --clear .venv
call :genPython > .venv\Lib\site-packages\gdal_env.py
goto :eof
:genPython
    echo import os
    echo import sys
    echo class gdal_env:
    echo     def __init__(self):
    echo         OSGEO_ROOT = 'C:\OSGeo4W64'.replace('\\', '\\')
    echo         os.environ['PATH']             = OSGEO_ROOT + '\\bin;' + os.environ['PATH']
    echo         os.environ['GDAL_DATA']        = OSGEO_ROOT + '\\share\\gdal'
    echo         os.environ['GDAL_DRIVER_PATH'] = OSGEO_ROOT + '\\bin\\gdalplugins'
    echo         os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + '\\share\\epsg_csv'
    echo         os.environ['PROJ_LIB']         = OSGEO_ROOT + '\\share\\proj'
    echo         self.OSGEO_ROOT = OSGEO_ROOT
    exit /b
