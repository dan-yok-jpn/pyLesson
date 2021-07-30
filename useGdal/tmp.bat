@echo off
cd "C:\Users\nkmanager\Desktop\pyLesson\useGdal\"
C:\OSGeo4W\apps\Python39\python.exe -m venv --system-site-packages --symlinks --without-pip --clear .venv
call :genPython > .venv\Lib\site-packages\gdal_env.py
goto :eof
:genPython
    echo import os
    echo class gdal_env:
    echo     def __init__(self):
    echo         OSGEO_ROOT = 'C:\OSGeo4W'.replace('\\', '\\')
    echo         OSGEO_BIN  = OSGEO_ROOT + '\\bin'
    echo         os.environ['PATH']             = OSGEO_BIN  + ';' + os.environ['PATH']
    echo         os.environ['GDAL_DATA']        = OSGEO_ROOT + '\\share\\gdal'
    echo         os.environ['GDAL_DRIVER_PATH'] = OSGEO_BIN  + '\\gdalplugins'
    echo         os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + '\\share\\epsg_csv'
    echo         os.environ['PROJ_LIB']         = OSGEO_ROOT + '\\share\\proj'
    echo         os.add_dll_directory(OSGEO_BIN)
    echo         self.OSGEO_ROOT = OSGEO_ROOT
    exit /b
