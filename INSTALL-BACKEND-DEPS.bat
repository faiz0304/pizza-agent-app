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

REM ========================================================================
REM  STEP 1: Validate Python Version
REM ========================================================================

echo [INFO] Checking Python version...

REM Get Python version from venv
if exist "venv\Scripts\python.exe" (
    for /f "tokens=2" %%i in ('venv\Scripts\python.exe --version 2^>^&1') do set PYTHON_VERSION=%%i
) else (
    echo [ERROR] Virtual environment not found!
    echo [ERROR] Run REBUILD-BACKEND-VENV.bat first
    pause
    exit /b 1
)

echo [INFO] Virtual environment Python: %PYTHON_VERSION%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

REM Block Python 3.12+
if %PYTHON_MAJOR% GEQ 3 (
    if %PYTHON_MINOR% GEQ 12 (
        echo.
        echo ========================================================================
        echo  [ERROR] INCOMPATIBLE PYTHON VERSION
        echo ========================================================================
        echo.
        echo Your venv is using Python %PYTHON_VERSION%
        echo This is NOT compatible with FastAPI/Pydantic ecosystem!
        echo.
        echo [SOLUTION] Rebuild your virtual environment:
        echo   1. Run: REBUILD-BACKEND-VENV.bat
        echo   2. Follow instructions to install Python 3.11.x
        echo.
        pause
        exit /b 1
    )
)

echo [OK] Python version is compatible
echo.

REM ========================================================================
REM  STEP 2: Activate and Install
REM ========================================================================

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [INFO] Installing dependencies from requirements.txt...
echo [INFO] This may take a few minutes...
echo.

REM Install numpy first to avoid conflicts
python -m pip install "numpy<2.0"

echo.
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo [ERROR] Check the error messages above
    echo.
    echo If you see pydantic-core build errors or Rust/Cargo:
    echo   - Your Python version is incompatible
    echo   - Run: REBUILD-BACKEND-VENV.bat
    echo.
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
