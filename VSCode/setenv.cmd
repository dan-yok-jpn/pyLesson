@echo off

If exist c:\osgeo4w64 (
    call :setenv c:\osgeo4w64
) else (
    For /d %%d in (c:\program~1\qgis*) do (
        set v=%%~sd
    )
    if "%v%"=="" (
        echo.
        echo ^ not installed QGIS
        exit 1
    )
    call :setenv %v%
)
goto :eof

:setenv %1
    for /d %%d in (%1\apps\Python3*) do (
        set v=%%d
    )
    if "%v%"=="" (
        echo.
        echo ^ QGIS is too old
        exit 1
    )
    set PYTHONHOME=%v%
    set PATH=%v%;%v%\Scripts;%PATH%
    rem set PYTHONHOME=%v%
    set v=
    exit /b
