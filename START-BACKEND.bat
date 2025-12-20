@echo off
REM Backend Server Startup Script - NumPy 2.0 Compatible
REM Double-click this file to start the backend server

echo ==========================================
echo Starting Backend Server
echo ==========================================
echo.

cd /d "%~dp0"
cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking ChromaDB NumPy compatibility...
python -c "import chromadb; print('✓ ChromaDB loaded successfully')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: ChromaDB import failed
    echo This may be a NumPy 2.0 compatibility issue
    pause
)

echo.
echo Starting Uvicorn server...
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
