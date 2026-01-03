@echo off
REM ========================================================================
REM  Pizza Agent App - Unified Startup Script
REM  Starts both Backend (FastAPI) and Frontend (Next.js) services
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo  PIZZA AGENT APP - UNIFIED STARTUP
echo ========================================================================
echo.

REM Get the project root directory
set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend"

echo [INFO] Project root: %PROJECT_ROOT%
echo.

REM ========================================================================
REM  STEP 1: Validate Environment
REM ========================================================================

echo [STEP 1] Validating environment...
echo.

REM Check if backend directory exists
if not exist "%BACKEND_DIR%" (
    echo [ERROR] Backend directory not found: %BACKEND_DIR%
    echo [ERROR] Please ensure you are running this from the project root
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "%FRONTEND_DIR%" (
    echo [ERROR] Frontend directory not found: %FRONTEND_DIR%
    echo [ERROR] Please ensure you are running this from the project root
    pause
    exit /b 1
)

REM Check if Python virtual environment exists
if not exist "%BACKEND_DIR%\venv\Scripts\activate.bat" (
    echo [ERROR] Python virtual environment not found
    echo [ERROR] Please create venv first: cd backend ^&^& python -m venv venv
    pause
    exit /b 1
)

REM Check if dependencies are installed (quick check for chromadb)
"%BACKEND_DIR%\venv\Scripts\python.exe" -c "import chromadb" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend dependencies not installed
    echo.
    echo [SOLUTION] Run this command first:
    echo   INSTALL-BACKEND-DEPS.bat
    echo.
    echo Or manually install dependencies:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Check if node_modules exists in frontend
if not exist "%FRONTEND_DIR%\node_modules" (
    echo [WARNING] node_modules not found in frontend
    echo [INFO] Will attempt to install dependencies on frontend startup
)

echo [OK] Environment validation complete
echo.

REM ========================================================================
REM  STEP 2: Start Backend Service
REM ========================================================================

echo [STEP 2] Starting backend service...
echo.

REM Create a temporary script for backend startup
set "BACKEND_SCRIPT=%TEMP%\start_backend_%RANDOM%.bat"

(
echo @echo off
echo cd /d "%BACKEND_DIR%"
echo echo.
echo echo ========================================================================
echo echo  BACKEND SERVICE - FastAPI on http://localhost:8000
echo echo ========================================================================
echo echo.
echo.
echo echo [INFO] Activating virtual environment...
echo call venv\Scripts\activate.bat
echo.
echo if errorlevel 1 ^(
echo     echo [ERROR] Failed to activate virtual environment
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [OK] Virtual environment activated
echo echo.
echo echo [INFO] Starting FastAPI server...
echo echo [INFO] API will be available at: http://localhost:8000
echo echo [INFO] Docs will be available at: http://localhost:8000/docs
echo echo.
echo echo Press Ctrl+C to stop the backend server
echo echo.
echo.
echo REM Start uvicorn server
echo python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
echo.
echo if errorlevel 1 ^(
echo     echo.
echo     echo [ERROR] Failed to start backend server
echo     echo [ERROR] Check if port 8000 is already in use
echo     pause
echo ^)
) > "%BACKEND_SCRIPT%"

REM Start backend in new window
start "Pizza Agent - Backend" cmd /k "%BACKEND_SCRIPT%"

echo [OK] Backend service started in separate window
echo [INFO] Backend will be available at: http://localhost:8000
echo.

REM Wait a moment for backend to initialize
echo [INFO] Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak >nul

REM ========================================================================
REM  STEP 3: Start Frontend Service
REM ========================================================================

echo [STEP 3] Starting frontend service...
echo.

REM Create a temporary script for frontend startup
set "FRONTEND_SCRIPT=%TEMP%\start_frontend_%RANDOM%.bat"

(
echo @echo off
echo cd /d "%FRONTEND_DIR%"
echo echo.
echo echo ========================================================================
echo echo  FRONTEND SERVICE - Next.js on http://localhost:3000
echo echo ========================================================================
echo echo.
echo.
echo REM Check if node_modules exists
echo if not exist "node_modules" ^(
echo     echo [WARNING] node_modules not found
echo     echo [INFO] Installing dependencies...
echo     echo.
echo     call npm install
echo     echo.
echo     if errorlevel 1 ^(
echo         echo [ERROR] Failed to install dependencies
echo         pause
echo         exit /b 1
echo     ^)
echo     echo [OK] Dependencies installed
echo     echo.
echo ^)
echo.
echo echo [INFO] Starting Next.js development server...
echo echo [INFO] Frontend will be available at: http://localhost:3000
echo echo.
echo echo Press Ctrl+C to stop the frontend server
echo echo.
echo.
echo REM Start Next.js dev server
echo npm run dev
echo.
echo if errorlevel 1 ^(
echo     echo.
echo     echo [ERROR] Failed to start frontend server
echo     echo [ERROR] Check if port 3000 is already in use
echo     pause
echo ^)
) > "%FRONTEND_SCRIPT%"

REM Start frontend in new window
start "Pizza Agent - Frontend" cmd /k "%FRONTEND_SCRIPT%"

echo [OK] Frontend service started in separate window
echo [INFO] Frontend will be available at: http://localhost:3000
echo.

REM ========================================================================
REM  STEP 4: Summary
REM ========================================================================

echo.
echo ========================================================================
echo  STARTUP COMPLETE
echo ========================================================================
echo.
echo [SUCCESS] Both services are starting up!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Both services are running in separate terminal windows.
echo To stop services, close their respective terminal windows or press Ctrl+C.
echo.
echo ========================================================================
echo.

REM Keep this window open for reference
echo Press any key to close this launcher window...
pause >nul

REM Cleanup temporary scripts (optional, will be cleaned by OS anyway)
if exist "%BACKEND_SCRIPT%" del "%BACKEND_SCRIPT%" >nul 2>&1
if exist "%FRONTEND_SCRIPT%" del "%FRONTEND_SCRIPT%" >nul 2>&1

endlocal
