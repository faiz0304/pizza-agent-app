@echo off
REM ========================================================================
REM  REBUILD BACKEND VIRTUAL ENVIRONMENT (Python 3.10 Required)
REM  Run this to completely rebuild your backend environment with
REM  Python 3.10 for stable Windows compatibility
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo  BACKEND VIRTUAL ENVIRONMENT REBUILD
echo ========================================================================
echo.

cd /d "%~dp0backend"

REM ========================================================================
REM  STEP 1: Find Python 3.10
REM ========================================================================

echo [STEP 1] Finding Python 3.10...
echo.

REM Try common Python 3.10 locations
set PYTHON310=

REM Try py launcher first (most reliable on Windows)
py -3.10 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON310=py -3.10
    for /f "tokens=2" %%i in ('py -3.10 --version') do set PYTHON_VERSION=%%i
    echo [OK] Found Python via py launcher: !PYTHON_VERSION!
    goto :python_found
)

REM Try python3.10 in PATH
python3.10 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON310=python3.10
    for /f "tokens=2" %%i in ('python3.10 --version') do set PYTHON_VERSION=%%i
    echo [OK] Found python3.10: !PYTHON_VERSION!
    goto :python_found
)

REM Try default python if it's 3.10
python --version 2>&1 | findstr "3.10" >nul
if %errorlevel% equ 0 (
    set PYTHON310=python
    for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [OK] Found Python 3.10 as default: !PYTHON_VERSION!
    goto :python_found
)

REM Python 3.10 not found
echo ========================================================================
echo  [ERROR] PYTHON 3.10 NOT FOUND
echo ========================================================================
echo.
echo This project requires Python 3.10 for Windows compatibility.
echo.
echo [DOWNLOAD PYTHON 3.10.11]:
echo   https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
echo.
echo [INSTALLATION INSTRUCTIONS]:
echo   1. Download the installer from the link above
echo   2. Run the installer
echo   3. CHECK "Add Python 3.10 to PATH"
echo   4. Complete installation
echo   5. Verify: py -3.10 --version
echo   6. Run this script again
echo.
echo ========================================================================
pause
exit /b 1

:python_found
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
REM  STEP 3: Create New Virtual Environment with Python 3.10
REM ========================================================================

echo [STEP 3] Creating new virtual environment with Python 3.10...
echo.

echo [INFO] Running: %PYTHON310% -m venv venv
%PYTHON310% -m venv venv

if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment created with Python 3.10
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
echo.

echo [INFO] Installing numpy first...
python -m pip install "numpy>=1.26,<2.0"

if errorlevel 1 (
    echo [ERROR] Failed to install numpy
    pause
    exit /b 1
)

echo [OK] numpy installed
echo.

echo [INFO] Installing all dependencies from requirements.txt...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo [ERROR] Check the error messages above
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

python -c "import sys; print('[OK] Python version:', sys.version.split()[0])"
python -c "import numpy; print('[OK] numpy:', numpy.__version__)"
python -c "import fastapi; print('[OK] fastapi')"
python -c "import pydantic; print('[OK] pydantic')"
python -c "import faiss; print('[OK] faiss')"
python -c "import uvicorn; print('[OK] uvicorn')"
python -c "import pymongo; print('[OK] pymongo')"

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
echo Virtual environment: backend\venv (Python 3.10)
echo.
echo Next steps:
echo   1. Run START-APP.bat to start the application
echo   2. Backend will be available at http://localhost:8000
echo.
pause
