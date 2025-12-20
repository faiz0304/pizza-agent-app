@echo off
REM Complete Startup and Testing Script for Windows
REM This script checks servers and runs tests

echo ==========================================
echo 🍕 Agentic Pizza System - Complete Startup
echo ==========================================
echo.

REM Step 1: Check if servers are running
echo Step 1: Checking if servers are already running...

curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Backend is running
    set BACKEND_RUNNING=true
) else (
    echo ⚠️  Backend is not running
    set BACKEND_RUNNING=false
)

curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Frontend is running
    set FRONTEND_RUNNING=true
) else (
    echo ⚠️  Frontend is not running
    set FRONTEND_RUNNING=false
)

echo.

REM Check if both servers are running
if "%BACKEND_RUNNING%"=="false" goto :need_servers
if "%FRONTEND_RUNNING%"=="false" goto :need_servers
goto :run_tests

:need_servers
echo =========================================
echo ⚠️  SERVERS NEED TO BE STARTED
echo =========================================
echo.

if "%BACKEND_RUNNING%"=="false" (
    echo To start the backend ^(Terminal 1^):
    echo   cd d:\Antigravity\pizza-agent-app\backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo   python seed_data.py
    echo   uvicorn main:app --reload
    echo.
)

if "%FRONTEND_RUNNING%"=="false" (
    echo To start the frontend ^(Terminal 2^):
    echo   cd d:\Antigravity\pizza-agent-app\frontend
    echo   npm install
    echo   npm run dev
    echo.
)

echo After starting servers, run this script again to execute tests.
pause
exit /b 1

:run_tests
echo Step 2: Running automated tests...
echo.

python run-tests.py

echo.
echo =========================================
echo ✅ Complete! Check results above.
echo =========================================
pause
