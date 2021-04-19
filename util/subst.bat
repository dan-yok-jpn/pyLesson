
: Substitute Sting

@echo off
setlocal

if "%1"=="" (goto :eof)
if "%2"=="" (goto :eof)
if "%3"=="" (goto :eof)

set command="Get-Content %1 | ForEach-Object {$_ -replace '%2','%3'}"

if exist %1 (
	powershell -NoProfile -ExecutionPolicy Unrestricted %command%
)
