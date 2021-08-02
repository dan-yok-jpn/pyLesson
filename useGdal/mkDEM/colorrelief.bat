: https://blog.code4history.dev/entry/20120923/1348413037

@echo off
setlocal

set PATH=c:\osgeo4w\bin
if "%1"=="" (
    set DEM=dem.tif
) else (
    set DEM=%1
)

call :genRamp > ramp.txt
gdaldem color-relief -of PNG -alpha %DEM% ramp.txt colorrelief.png
del ramp.txt
goto :eof

:genRamp
    echo nv 0 0 0 0
    echo 0%% 0 0 205
    echo 4%% 0 191 191
    echo 9%% 57 151 105
    echo 16%% 117 194 93
    echo 25%% 230 230 128
    echo 36%% 202 158 75
    echo 49%% 214 187 98
    echo 64%% 185 154 100
    echo 81%% 220 220 220
    echo 100%% 255 255 255
    exit /b