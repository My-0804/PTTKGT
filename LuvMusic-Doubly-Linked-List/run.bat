@echo off
title LuvMusic
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    set "PYTHON_CMD=python"
) else (
    set "PYTHON_CMD=py"
)

echo [1/2] Dang cai dat thu vien can thiet...
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Khong the cai dat thu vien. Hay cai Python 3 va chon Add Python to PATH.
    pause
    exit /b 1
)

echo [2/2] Dang khoi dong LuvMusic tai http://localhost:5000
start "" cmd /c "timeout /t 3 /nobreak ^>nul ^& start http://localhost:5000"
%PYTHON_CMD% app.py
pause
