# 🚀 Quick Start Guide
## Agentic Pizza Ordering System

**Time Required**: 2 minutes  
**Complexity**: Very Easy ✨

---

## ⚡ Super Quick Start (3 Steps)

### Step 1: Start Backend (Double-Click)
📁 **File**: `START-BACKEND.bat`

Just double-click this file. A terminal window will open showing:
```
Starting Backend Server
Activating virtual environment...
Starting Uvicorn server...
Backend will be available at: http://localhost:8000
```

✅ Keep this window **open and running**

---

### Step 2: Start Frontend (Double-Click)
📁 **File**: `START-FRONTEND.bat`

Just double-click this file. A terminal window will open showing:
```
Starting Frontend Server
Starting Next.js development server...
Frontend will be available at: http://localhost:3000
```

✅ Keep this window **open and running**

---

### Step 3: Run Tests (Double-Click)
📁 **File**: `RUN-TESTS.bat`

Wait ~10 seconds for servers to fully start, then double-click this file.

Expected output:
```
✓ Backend is running
✓ Frontend is running

Both servers detected. Running tests...

🍕 Agentic Pizza Testing Suite
✅ Passed: 12
❌ Failed: 0
🎉 All tests passed!
```

---

## 🌐 Access the Application

Once servers are running:

| What | URL |
|------|-----|
| **Frontend Website** | http://localhost:3000 |
| **Chat with Agent** | http://localhost:3000/chat |
| **Browse Menu** | http://localhost:3000/menu |
| **View Cart** | http://localhost:3000/cart |
| **Track Orders** | http://localhost:3000/order |
| **Backend API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

---

## 🛑 Stopping the Servers

1. Click on the backend terminal window
2. Press `Ctrl+C`
3. Click on the frontend terminal window
4. Press `Ctrl+C`

---

## 🐛 Troubleshooting

### "Backend is not running" error
**Solution**: Make sure `START-BACKEND.bat` terminal is still open and showing server logs

### "Frontend is not running" error
**Solution**: Make sure `START-FRONTEND.bat` terminal is still open and showing server logs

### "Port already in use" error
**Solution**: 
1. Close any existing server terminals
2. Wait 5 seconds
3. Restart the servers

### Tests fail
**Solution**:
1. Wait 10-15 seconds after starting servers
2. Check both terminal windows show servers are running
3. Visit http://localhost:8000/health to verify backend
4. Visit http://localhost:3000 to verify frontend

---

## 📝 Manual Commands (Optional)

If you prefer using PowerShell/CMD manually:

**Terminal 1** (Backend):
```powershell
cd d:\Antigravity\pizza-agent-app\backend
venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2** (Frontend):
```powershell
cd d:\Antigravity\pizza-agent-app\frontend
npm run dev
```

**Terminal 3** (Tests):
```powershell
cd d:\Antigravity\pizza-agent-app
python run-tests.py
```

---

## ✅ Success Indicators

Backend is ready when you see:
```
✅ Application startup complete
```

Frontend is ready when you see:
```
ready started server on 0.0.0.0:3000
```

Tests passed when you see:
```
✅ Passed: 12
❌ Failed: 0
```

---

**That's it! Your pizza ordering system is running! 🍕🤖**
