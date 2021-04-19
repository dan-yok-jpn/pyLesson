
: Write Out Text within Clipboard to Standard Output

@echo off

powershell -NoProfile -ExecutionPolicy Unrestricted "Get-Clipboard -Format Text"
