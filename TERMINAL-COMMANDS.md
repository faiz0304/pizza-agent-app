# 🚀 TERMINAL STARTUP COMMANDS
# Copy-paste these commands into separate terminals

## Terminal 1: Backend Server

### First Time Setup (Only Run Once)
cd d:\Antigravity\pizza-agent-app\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py

### Start Backend Server (Run Every Time)
cd d:\Antigravity\pizza-agent-app\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000

## Expected Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     🚀 Starting Agentic Pizza Ordering System...
# INFO:     ✅ Connected to MongoDB: pizza_db
# INFO:     ✅ Knowledge base initialized with 12 entries
# INFO:     ✅ Application startup complete

---

## Terminal 2: Frontend Server

### First Time Setup (Only Run Once)
cd d:\Antigravity\pizza-agent-app\frontend
npm install

### Start Frontend Server (Run Every Time)
cd d:\Antigravity\pizza-agent-app\frontend
npm run dev

## Expected Output:
# ▲ Next.js 14.1.0
# - Local:        http://localhost:3000
# - ready started server on 0.0.0.0:3000

---

## Terminal 3: Run Tests (After Both Servers Started)

### First Time Setup (Only Run Once)
cd d:\Antigravity\pizza-agent-app
pip install -r test-requirements.txt

### Run Automated Tests
cd d:\Antigravity\pizza-agent-app
python run-tests.py

## Expected Output:
# ==================================================
# 🍕 Agentic Pizza Testing Suite
# ==================================================
# 
# 📡 Server Status Tests
# --------------------------------------------------
# Testing: Backend Health ... ✅ PASS
# Testing: Frontend Accessible ... ✅ PASS
# 
# ... (16 more tests)
# 
# ✅ Passed: 18
# ❌ Failed: 0
# 
# 🎉 All tests passed!

---

## Quick Commands (If Already Setup)

# Terminal 1
cd d:\Antigravity\pizza-agent-app\backend && venv\Scripts\activate && uvicorn main:app --reload

# Terminal 2
cd d:\Antigravity\pizza-agent-app\frontend && npm run dev

# Terminal 3 (wait 10 seconds after Terminal 1 & 2)
cd d:\Antigravity\pizza-agent-app && python run-tests.py

---

## Troubleshooting

### If Backend Fails to Start:
# Check .env file exists and has valid MongoDB URI
# Verify: d:\Antigravity\pizza-agent-app\backend\.env

### If Frontend Fails to Start:
# Delete node_modules and reinstall
cd d:\Antigravity\pizza-agent-app\frontend
Remove-Item -Recurse -Force node_modules
npm install

### If Tests Fail:
# Ensure both servers are running
# Check http://localhost:8000/health in browser
# Check http://localhost:3000 in browser

---

## After Successful Tests

# Open browser and manually test:
# http://localhost:3000        - Landing page
# http://localhost:3000/chat   - Chat with agent
# http://localhost:3000/menu   - Browse menu
# http://localhost:3000/cart   - View cart
# http://localhost:3000/order  - Track orders

---

## Stopping Servers

# In Terminal 1 (Backend): Press Ctrl+C
# In Terminal 2 (Frontend): Press Ctrl+C
