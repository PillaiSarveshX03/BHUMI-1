@echo off
echo =========================================
echo       Starting BHUMI Application
echo =========================================
echo.

:: Check if the virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [1/3] Virtual environment not found. Creating one now...
    python -m venv venv
    
    echo [2/3] Activating virtual environment and installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
) else (
    echo [1/2] Activating existing virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Opening BHUMI frontend in your default browser...
start "" "index.html"

echo.
echo Starting Flask backend server...
echo Press CTRL+C in this window to stop the server.
echo.
python backend\app.py

pause
