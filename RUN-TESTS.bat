@echo off
REM Test Runner with Cache Clear
REM Clears Python cache before running tests

echo ==========================================
echo Running Automated Tests (Cache Cleared)
echo ==========================================
echo.

cd /d "%~dp0"

REM Clear Python cache
echo Clearing Python cache...
if exist __pycache__ rd /s /q __pycache__
if exist run-tests.pyc del /f /q run-tests.pyc
echo.

echo Checking if servers are running...
echo.

REM Check backend
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Backend server is not running!
    echo Please start START-BACKEND.bat first
    echo.
    pause
    exit /b 1
)
echo ✓ Backend is running

REM Check frontend
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Frontend server is not running!
    echo Please start START-FRONTEND.bat first
    echo.
    pause
    exit /b 1
)
echo ✓ Frontend is running

echo.
echo Both servers detected. Running tests...
echo.

REM Run fresh tests
python -B run-tests.py

echo.
pause
