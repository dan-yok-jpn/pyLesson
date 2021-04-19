
: Set up the environment for Visual Studio Code

@echo off
setlocal

set dst_dir=%APPDATA%\Code\User

copy launch.json %dst_dir% 1>nul 2>&1

If exist c:\osgeo4w64 (
    call :mkJSON c:\osgeo4w64
) else (
    For /d %%d in (c:\program~1\qgis*) do (
        set v=%%~sd
    )
    if "%v%"=="" (
        echo.
        echo ^ not installed QGIS
        goto :eof
    )
    call :mkJSON %v%
)
                goto :eof
:mkJSON %1
    for /d %%d in (%1\apps\Python3*) do (
        set v=%%d
    )
    if "%v%"=="" (
        echo.
        echo ^ QGIS is too old
        exit /b
    )
    call subst.bat template _PYTHONHOME_ %v% > tmp
    call subst.bat tmp       \\          \\  > %dst_dir%\settings.json
    del tmp
    exit /b
