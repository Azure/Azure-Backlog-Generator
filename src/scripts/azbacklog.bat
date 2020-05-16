@echo off
setlocal

SET PYTHONPATH=%~dp0\src;%PYTHONPATH%

IF EXIST "%~dp0\python.exe" (
  "%~dp0\python.exe" -m azbacklog %*
) ELSE (
  python -m azbacklog %*
)