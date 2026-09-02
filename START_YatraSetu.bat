@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo       YatraSetu - Local Web App
echo ========================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    set "PY=python"
)

echo Installing required packages (first run may take a moment)...
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Could not install the required packages.
    echo Make sure Python is installed and try again.
    pause
    exit /b 1
)

echo.
echo Starting YatraSetu...
start "YatraSetu Browser" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"
%PY% app.py
pause
