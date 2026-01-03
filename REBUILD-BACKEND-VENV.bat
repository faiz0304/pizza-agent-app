@echo off
REM ========================================================================
REM  REBUILD BACKEND VIRTUAL ENVIRONMENT
REM  Run this to completely rebuild your backend environment with
REM  a supported Python version (3.10.x or 3.11.x)
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo  BACKEND VIRTUAL ENVIRONMENT REBUILD
echo ========================================================================
echo.

cd /d "%~dp0backend"

REM ========================================================================
REM  STEP 1: Validate Python Version
REM ========================================================================

echo [STEP 1] Validating Python version...
echo.

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

echo [INFO] Detected Python version: %PYTHON_VERSION%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

echo [INFO] Python %PYTHON_MAJOR%.%PYTHON_MINOR%
echo.

REM Check if Python 3.12 or higher
if %PYTHON_MAJOR% GEQ 3 (
    if %PYTHON_MINOR% GEQ 12 (
        echo ========================================================================
        echo  [ERROR] UNSUPPORTED PYTHON VERSION DETECTED
        echo ========================================================================
        echo.
        echo Your Python version: %PYTHON_VERSION%
        echo Supported versions:  3.10.x or 3.11.x
        echo.
        echo [REASON] Python 3.12+ is NOT compatible with FastAPI ecosystem
        echo          - pydantic-core has no stable wheels for Python 3.12+
        echo          - chromadb breaks on Python 3.12+
        echo          - Attempting installation triggers Rust compilation
        echo.
        echo [SOLUTION] Install Python 3.11.x:
        echo.
        echo   1. Download Python 3.11.9 for Windows x64:
        echo      https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
        echo.
        echo   2. During installation:
        echo      - Check "Add Python to PATH"
        echo      - Select "Install for all users" (optional)
        echo.
        echo   3. After installation, verify:
        echo      python --version
        echo      (Should show Python 3.11.x)
        echo.
        echo   4. Re-run this script
        echo.
        echo ========================================================================
        pause
        exit /b 1
    )
)

REM Check if Python version is too old
if %PYTHON_MAJOR% LSS 3 (
    echo [ERROR] Python 3.10 or 3.11 is required
    echo [ERROR] Your version: %PYTHON_VERSION%
    pause
    exit /b 1
)

if %PYTHON_MAJOR% EQU 3 (
    if %PYTHON_MINOR% LSS 10 (
        echo [ERROR] Python 3.10 or 3.11 is required
        echo [ERROR] Your version: %PYTHON_VERSION%
        pause
        exit /b 1
    )
)

echo [OK] Python version is supported (%PYTHON_VERSION%)
echo.

REM ========================================================================
REM  STEP 2: Remove Old Virtual Environment
REM ========================================================================

echo [STEP 2] Cleaning old virtual environment...
echo.

if exist "venv" (
    echo [INFO] Removing old venv directory...
    rmdir /s /q venv
    if errorlevel 1 (
        echo [ERROR] Failed to remove old venv
        echo [ERROR] Close any programs using the venv and try again
        pause
        exit /b 1
    )
    echo [OK] Old venv removed
) else (
    echo [INFO] No existing venv found
)

echo.

REM ========================================================================
REM  STEP 3: Create New Virtual Environment
REM ========================================================================

echo [STEP 3] Creating new virtual environment...
echo.

echo [INFO] Running: python -m venv venv
python -m venv venv

if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment created
echo.

REM ========================================================================
REM  STEP 4: Upgrade pip, setuptools, wheel
REM ========================================================================

echo [STEP 4] Upgrading core tools...
echo.

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip tools (continuing anyway)
)

echo [OK] Core tools upgraded
echo.

REM ========================================================================
REM  STEP 5: Install Dependencies
REM ========================================================================

echo [STEP 5] Installing dependencies...
echo.

echo [INFO] This may take several minutes...
echo [INFO] Installing numpy first to avoid conflicts...
python -m pip install "numpy<2.0"

echo.
echo [INFO] Installing all dependencies from requirements.txt...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo [ERROR] Check the error messages above
    echo.
    echo Common issues:
    echo - Internet connection required
    echo - Firewall blocking pip downloads
    echo - Disk space insufficient
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully
echo.

REM ========================================================================
REM  STEP 6: Verify Installation
REM ========================================================================

echo [STEP 6] Verifying installation...
echo.

echo [INFO] Testing critical imports...

python -c "import fastapi; print('[OK] fastapi imported')"
python -c "import pydantic; print('[OK] pydantic imported')"
python -c "import chromadb; print('[OK] chromadb imported')"
python -c "import uvicorn; print('[OK] uvicorn imported')"

if errorlevel 1 (
    echo [ERROR] Import verification failed
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo  REBUILD COMPLETE
echo ========================================================================
echo.
echo [SUCCESS] Backend environment rebuilt successfully!
echo.
echo Python version: %PYTHON_VERSION%
echo Virtual environment: backend\venv
echo.
echo Next steps:
echo   1. Run START-APP.bat to start the application
echo   2. Backend will be available at http://localhost:8000
echo.
pause
