@echo off
REM ========================================================================
REM  Install Backend Dependencies (Python 3.12 Compatible)
REM  Installs all required packages using prebuilt wheels
REM ========================================================================

echo.
echo ========================================================================
echo  INSTALLING BACKEND DEPENDENCIES
echo ========================================================================
echo.

cd /d "%~dp0backend"

REM ========================================================================
REM  STEP 1: Validate Virtual Environment
REM ========================================================================

echo [INFO] Checking virtual environment...

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo [ERROR] Create it first: python -m venv venv
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('venv\Scripts\python.exe --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Using Python %PYTHON_VERSION%
echo.

REM ========================================================================
REM  STEP 2: Upgrade pip and core tools
REM ========================================================================

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [INFO] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel --quiet

if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip tools (continuing anyway)
)

echo [OK] Core tools upgraded
echo.

REM ========================================================================
REM  STEP 3: Install Dependencies
REM ========================================================================

echo [INFO] Installing dependencies from requirements.txt...
echo [INFO] This may take a few minutes...
echo.

REM Strategy: Install numpy first, then everything else
echo [STEP 3.1] Installing numpy...
python -m pip install "numpy<2.0" --only-binary=:all:

if errorlevel 1 (
    echo [ERROR] Failed to install numpy
    pause
    exit /b 1
)

echo [OK] numpy installed
echo.

echo [STEP 3.2] Installing all other dependencies...
python -m pip install -r requirements.txt --prefer-binary

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo [ERROR] Check the error messages above
    echo.
    echo If you see build errors:
    echo   1. Ensure you have the latest pip: pip install --upgrade pip
    echo   2. Try: pip install -r requirements.txt --only-binary=:all:
    echo.
    pause
    exit /b 1
)

echo [OK] All dependencies installed
echo.

REM ========================================================================
REM  STEP 4: Verify Installation
REM ========================================================================

echo [INFO] Verifying critical imports...

python -c "import fastapi; print('[OK] fastapi')" || goto :error
python -c "import pydantic; print('[OK] pydantic')" || goto :error
python -c "import chromadb; print('[OK] chromadb')" || goto :error
python -c "import uvicorn; print('[OK] uvicorn')" || goto :error
python -c "import pymongo; print('[OK] pymongo')" || goto :error

echo.
echo ========================================================================
echo  INSTALLATION COMPLETE
echo ========================================================================
echo.
echo [SUCCESS] All backend dependencies installed successfully!
echo.
echo Python version: %PYTHON_VERSION%
echo You can now run START-APP.bat to start the application.
echo.
pause
exit /b 0

:error
echo.
echo [ERROR] Import verification failed
echo [ERROR] Some packages did not install correctly
pause
exit /b 1
