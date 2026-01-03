@echo off
REM ========================================================================
REM  Quick Fix: Install Backend Dependencies
REM  Run this if you get "ModuleNotFoundError" when starting the backend
REM ========================================================================

echo.
echo ========================================================================
echo  INSTALLING BACKEND DEPENDENCIES
echo ========================================================================
echo.

cd /d "%~dp0backend"

echo [INFO] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [INFO] Installing dependencies from requirements.txt...
echo [INFO] This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo [ERROR] Check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo  INSTALLATION COMPLETE
echo ========================================================================
echo.
echo [SUCCESS] All backend dependencies installed successfully!
echo.
echo You can now run START-APP.bat to start the application.
echo.
pause
