@echo off
echo =========================================
echo       Stopping BHUMI Application
echo =========================================
echo.
echo Stopping any server listening on port 5000...

for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do (
    echo Killing process %%a...
    taskkill /F /PID %%a
)

echo.
echo Server stopped successfully!
pause
