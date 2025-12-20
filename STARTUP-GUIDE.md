# Server Startup & Testing Guide

## 🚀 Quick Start (Windows)

### Option 1: Automatic Startup Check
```cmd
cd d:\Antigravity\pizza-agent-app
start-and-test.bat
```

This script will:
- ✅ Check if servers are running
- ✅ Provide startup commands if needed
- ✅ Run all automated tests when ready

### Option 2: Manual Startup

**Terminal 1 - Backend**:
```cmd
cd d:\Antigravity\pizza-agent-app\backend

REM First time only
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py

REM Every time
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```cmd
cd d:\Antigravity\pizza-agent-app\frontend

REM First time only
npm install

REM Every time
npm run dev
```

**Terminal 3 - Run Tests**:
```cmd
cd d:\Antigravity\pizza-agent-app
pip install -r test-requirements.txt
python run-tests.py
```

---

## ✅ Expected Output

### Backend Startup
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     🚀 Starting Agentic Pizza Ordering System...
INFO:     ✅ Connected to MongoDB: pizza_db
INFO:     ✅ Knowledge base initialized with 12 entries
INFO:     ✅ Application startup complete
```

### Frontend Startup
```
▲ Next.js 14.1.0
- Local:        http://localhost:3000
- ready started server on 0.0.0.0:3000
```

### Test Execution
```
==================================================
🍕 Agentic Pizza Testing Suite
==================================================

📡 Server Status Tests
--------------------------------------------------
Testing: Backend Health ... ✅ PASS
Testing: Frontend Accessible ... ✅ PASS

🔧 Backend API Tests
--------------------------------------------------
Testing: Menu Listing ... ✅ PASS
Testing: Menu Search ... ✅ PASS
Testing: Chatbot Greeting ... ✅ PASS
Testing: Chatbot Menu Search ... ✅ PASS
Testing: Chatbot KB Search ... ✅ PASS

🌐 Frontend Page Tests
--------------------------------------------------
Testing: Landing Page ... ✅ PASS
Testing: Chat Page ... ✅ PASS
Testing: Menu Page ... ✅ PASS
Testing: Cart Page ... ✅ PASS
Testing: Order Page ... ✅ PASS

==================================================
📊 Test Results Summary
==================================================

✅ Passed: 12
❌ Failed: 0

🎉 All tests passed!
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError`
```cmd
pip install -r requirements.txt
```

**Error**: `MongoDB connection failed`
- Check `.env` file has valid `MONGODB_URI`
- Verify MongoDB Atlas IP whitelist
- Test connection string in MongoDB Compass

**Error**: `Port 8000 already in use`
```cmd
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Frontend Won't Start

**Error**: `Module not found`
```cmd
rm -rf node_modules package-lock.json
npm install
```

**Error**: `Port 3000 already in use`
```cmd
# Find and kill process
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

### Tests Failing

**Connection Refused**
- Ensure both servers are running
- Check ports 8000 and 3000 are accessible
- Verify no firewall blocking

**Test Timeout**
- Increase timeout in run-tests.py
- Check backend logs for slow queries
- Verify HuggingFace API token validity

---

## 📊 Monitoring During Tests

### Watch Backend Logs
```cmd
# In backend terminal, you'll see:
INFO:     127.0.0.1:xxxxx - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /menu HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /chatbot HTTP/1.1" 200 OK
INFO:     🤖 Agent decided to use tool: search_menu
INFO:     ✅ Tool execution successful
```

### Watch Frontend Logs
```cmd
# In frontend terminal, you'll see:
GET / 200 in 45ms
GET /chat 200 in 23ms
GET /menu 200 in 31ms
```

---

## 🎯 Post-Testing Actions

After successful tests:

1. **Keep servers running** for manual testing
2. **Open browser**: http://localhost:3000
3. **Test UI manually** (see TESTING-CHECKLIST.md)
4. **Check monitoring** (see MONITORING.md)

---

## 📚 Additional Resources

- Full Testing Guide: [TESTING.md](TESTING.md)
- Quick Checklist: [TESTING-CHECKLIST.md](TESTING-CHECKLIST.md)
- Monitoring Setup: [MONITORING.md](MONITORING.md)
- Deployment Guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Ready to start!** Run `start-and-test.bat` 🚀
