@echo off
REM ========================================================================
REM  Install Backend Dependencies (Python 3.12 Compatible - Windows)
REM  Installs all required packages using prebuilt wheels ONLY
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
    echo [ERROR] Run: REBUILD-BACKEND-VENV.bat
    pause
    exit /b 1
)

REM Get and validate Python version
for /f "tokens=2" %%i in ('venv\Scripts\python.exe --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Virtual environment Python: %PYTHON_VERSION%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

REM Check if Python 3.10
if not "%PYTHON_MAJOR%"=="3" goto :version_error
if not "%PYTHON_MINOR%"=="10" goto :version_error

echo [OK] Python 3.10 confirmed
echo.
goto :upgrade_pip

:version_error
echo.
echo ========================================================================
echo  [ERROR] INCOMPATIBLE PYTHON VERSION
echo ========================================================================
echo.
echo Your venv is using Python %PYTHON_VERSION%
echo This project requires Python 3.10.x
echo.
echo [SOLUTION] Rebuild your virtual environment:
echo   1. Install Python 3.10.11
echo   2. Run: REBUILD-BACKEND-VENV.bat
echo.
pause
exit /b 1

:upgrade_pip

REM ========================================================================
REM  STEP 2: Upgrade pip and core tools
REM ========================================================================

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [INFO] Checking pip version...
for /f "tokens=2" %%i in ('python -m pip --version') do set PIP_VERSION=%%i
echo [INFO] Current pip: %PIP_VERSION%

echo [INFO] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip tools (continuing anyway)
) else (
    for /f "tokens=2" %%i in ('python -m pip --version') do set NEW_PIP_VERSION=%%i
    echo [OK] pip upgraded to: %NEW_PIP_VERSION%
)

echo.

REM ========================================================================
REM  STEP 3: Install Dependencies (BINARY ONLY - No Source Compilation)
REM ========================================================================

echo [INFO] Installing dependencies from requirements.txt...
echo [INFO] Using BINARY WHEELS ONLY (no source compilation)
echo [INFO] This may take a few minutes...
echo.

REM Critical: Install numpy first with binary-only flag
echo [STEP 3.1] Installing numpy (binary wheel)...
echo [INFO] Searching for numpy ^>=1.26,^<2.0 with Python 3.12 wheels...
echo [INFO] Forcing binary installation to avoid GCC/Rust compilation...

python -m pip install "numpy>=1.26,<2.0" --only-binary=numpy

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install numpy binary wheel
    echo.
    echo Troubleshooting:
    echo   1. Clear pip cache: pip cache purge
    echo   2. Try specific version: pip install numpy==1.26.3 --only-binary=numpy
    echo   3. Check internet: ping pypi.org
    echo   4. Upgrade pip: python -m pip install --upgrade pip
    echo.
    pause
    exit /b 1
)

REM Verify numpy installation
python -c "import numpy; print('[OK] numpy version:', numpy.__version__)"

if errorlevel 1 (
    echo [ERROR] numpy installed but cannot import
    pause
    exit /b 1
)
echo.

REM Install all other dependencies
echo [STEP 3.2] Installing all other dependencies...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo [ERROR] Check the error messages above
    echo.
    echo If you see build errors:
    echo   - Clear cache: pip cache purge
    echo   - Reinstall: pip install -r requirements.txt --force-reinstall
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

python -c "import numpy; print('[OK] numpy version:', numpy.__version__)" || goto :error
python -c "import fastapi; print('[OK] fastapi')" || goto :error
python -c "import pydantic; print('[OK] pydantic')" || goto :error
python -c "import faiss; print('[OK] faiss')" || goto :error
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
echo Installation method: Binary wheels only (no source compilation)
echo.
echo You can now run START-APP.bat to start the application.
echo.
pause
exit /b 0

:error
echo.
echo [ERROR] Import verification failed
echo [ERROR] Some packages did not install correctly
echo.
echo Please try:
echo   1. Delete venv: rmdir /s /q venv
echo   2. Recreate: python -m venv venv
echo   3. Run this script again
echo.
pause
exit /b 1
