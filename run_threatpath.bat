@echo off
title ThreatPath - L&T TECHgium Presentation Prototype
color 0B

:: Default port 5000
set PORT=5000
if not "%~1"=="" set PORT=%~1

echo ===============================================================================
echo   THREATPATH: AI-Assisted Threat Modeling and Security Validation
echo   10th Edition L^&T TECHgium Presentation Round - PID: TG0915208
echo   PSNA College of Engineering and Technology, Dindigul
echo ===============================================================================
echo.
echo [*] Target Port: %PORT%
echo [*] Initializing ThreatPath Core Engine and Virtual CAN Simulator...
cd /d "%~dp0threatpath\backend"

echo.
echo [*] Server is starting up...
echo [!] IMPORTANT: KEEP THIS COMMAND PROMPT WINDOW OPEN!
echo     Closing this window stops the prototype server.
echo.

:: Wait 2 seconds for Python/Uvicorn to bind before opening the browser
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:%PORT%"

:: Launch Uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port %PORT%

pause
