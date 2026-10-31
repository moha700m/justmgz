@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY (where python >nul 2>&1 && set "PY=python")
if not defined PY (echo Python not found & pause & exit /b 1)
%PY% -m jmz %*
pause
