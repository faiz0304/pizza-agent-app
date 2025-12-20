@echo off
REM Frontend Server Startup Script
REM Double-click this file to start the frontend server

echo ==========================================
echo Starting Frontend Server
echo ==========================================
echo.

cd /d "%~dp0"
cd frontend

echo.
echo Starting Next.js development server...
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

npm run dev

pause
