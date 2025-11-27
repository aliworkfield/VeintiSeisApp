@echo off
REM One-click launcher for Windows that runs the PowerShell test helper with a permissive ExecutionPolicy so users on RemoteSigned systems can run the script.
REM Usage: double-click this file or run in an elevated or non-elevated command prompt:
REM   scripts\test-local.cmd

set SCRIPT_DIR=%~dp0
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& '%SCRIPT_DIR%test-local.ps1' %*"
