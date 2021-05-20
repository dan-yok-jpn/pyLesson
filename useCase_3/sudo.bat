@echo off
powershell.exe Start-Process "%1" -Verb runas 
@echo on