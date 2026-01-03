# START-APP.bat - Unified Application Startup

## Overview

`START-APP.bat` is a Windows batch script that starts both the **backend** (FastAPI) and **frontend** (Next.js) services with a single command.

## Features

✅ **Automated Environment Validation**
- Checks for backend/frontend directories
- Validates Python virtual environment
- Detects missing node_modules and offers to install

✅ **Separate Terminal Windows**
- Backend runs in its own terminal
- Frontend runs in its own terminal
- Easy to monitor logs separately

✅ **Error Handling**
- Clear error messages
- Graceful failure with instructions
- Port conflict detection

✅ **User-Friendly Output**
- Status messages for each step
- Service URLs displayed clearly
- Instructions on how to stop services

## Usage

### Quick Start

1. Open Command Prompt or PowerShell
2. Navigate to the project root:
   ```cmd
   cd D:\Antigravity_pizza_agent\pizza-agent-app
   ```
3. Run the startup script:
   ```cmd
   START-APP.bat
   ```

### What Happens

1. **Environment Validation**: Checks if all required directories and files exist
2. **Backend Startup**: Launches FastAPI server on `http://localhost:8000` in a new window
3. **Frontend Startup**: Launches Next.js dev server on `http://localhost:3000` in a new window
4. **Summary**: Displays service URLs and status

### After Startup

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

Both services will run in separate terminal windows. Each window shows real-time logs.

## Stopping Services

### Option 1: Close Terminal Windows
Simply close the "Pizza Agent - Backend" and "Pizza Agent - Frontend" terminal windows.

### Option 2: Press Ctrl+C
In each terminal window, press `Ctrl+C` to stop the service gracefully.

## Troubleshooting

### Error: Virtual environment not found
```
[ERROR] Python virtual environment not found
```
**Solution**: Create the virtual environment:
```cmd
cd backend
python -m venv venv
```

### Error: Port already in use
```
[ERROR] Failed to start backend/frontend server
[ERROR] Check if port 8000/3000 is already in use
```
**Solution**: Stop any existing services using those ports or change the port in the respective configuration files.

### Error: node_modules not found
The script will automatically detect this and run `npm install` in the frontend window. Allow it to complete before accessing the frontend.

## Requirements

- **Windows OS**: This is a Windows batch script (`.bat`)
- **Python 3.8+**: With virtual environment created in `backend/venv`
- **Node.js 14+**: For Next.js frontend
- **Backend dependencies**: Installed in virtual environment
- **Frontend dependencies**: Will be installed automatically if missing

## Alternative Scripts

If you prefer to start services individually:

- **Backend only**: Use `backend/START-BACKEND.bat`
- **Frontend only**: Use `frontend/START-FRONTEND.bat` (if exists)

## Technical Details

### Backend Startup Process
1. Navigate to `backend/` directory
2. Activate Python virtual environment
3. Start Uvicorn server with auto-reload
4. Listen on `0.0.0.0:8000`

### Frontend Startup Process
1. Navigate to `frontend/` directory
2. Check for `node_modules/`
3. Run `npm install` if needed
4. Start Next.js dev server with `npm run dev`
5. Listen on `localhost:3000`

### Terminal Windows
The script creates temporary batch files in `%TEMP%` directory to launch each service in a separate CMD window. These temporary files are cleaned up when the launcher closes.

## Integration with Development Workflow

This script is ideal for:
- **Local development**: Quick setup without manual steps
- **Testing**: Start full stack with one command
- **Demonstrations**: Reliable startup for presentations
- **Onboarding**: New developers can start the app easily

## Support

For issues or questions:
1. Check the terminal windows for error messages
2. Review the troubleshooting section above
3. Ensure all prerequisites are installed
4. Check GitHub repository issues

---

**Note**: This script is designed for Windows development environments. For Linux/Mac, please use shell scripts or npm scripts instead.
