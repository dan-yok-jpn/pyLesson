@echo off
setlocal

if "%1"=="-h" (
	echo.
	echo ^ Create Visual Studio startup file for Python
	echo.
	echo ^   Usage : %~n0 [-h] [name] [name.py]
	goto :eof
)
if "%1"=="" (
	echo.
	echo ^ #### WARNNING #### must be supplied name of project
	goto :eof
)

if "%~x1"==".py" (set dst=%~n1) else (set dst=%1)

if exist .vs (del /s /q .vs)

if not exist %dst%.py (echo print^('Hello World'^) > %dst%.py)

call :genProj %dst% > %dst%.pyproj
								goto :eof
:genProj %1
	set prj=$(MSBuildExtensionsPath32)\Microsoft\VisualStudio
	set prj=%prj%\v$(VisualStudioVersion)
	set prj=%prj%\Python Tools\Microsoft.PythonTools.targets

	echo ^<Project ToolsVersion="4.0"^>
	echo   ^<PropertyGroup^>
	echo     ^<StartupFile^>%1.py^</StartupFile^>
	echo     ^<Name^>%1^</Name^>
	echo     ^<RootNamespace^>%1^</RootNamespace^>
	echo   ^</PropertyGroup^>
	echo   ^<ItemGroup^>
	echo     ^<Compile Include="%1.py" /^>
	echo   ^</ItemGroup^>
	echo   ^<Import Project="%prj%" /^>
	echo ^</Project^>
	exit /b
