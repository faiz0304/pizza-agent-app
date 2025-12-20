# 🎯 MANUAL EXECUTION CHECKLIST
## Agentic Pizza Ordering System

**Time Required**: 15-20 minutes (first time)  
**Date**: 2025-12-05

---

## ✅ PRE-FLIGHT CHECKLIST

### Environment Check
- [ ] Backend `.env` file exists with MongoDB URI and HuggingFace token
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] 3 terminal windows ready

---

## 📋 STEP-BY-STEP EXECUTION

### STEP 1: Backend Environment Setup (5 min)

**Terminal 1** - Open PowerShell/CMD:

```powershell
# Navigate to backend
cd d:\Antigravity\pizza-agent-app\backend

# Create .env file if it doesn't exist
copy .env.example .env
notepad .env
```

**In notepad**, add your credentials:
```env
MONGODB_URI=your_mongodb_connection_string
HUGGINGFACE_API_TOKEN=your_hf_token
```

Save and close.

**Continue in Terminal 1**:
```powershell
# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Seed database (first time only)
python seed_data.py
```

**Expected Output**:
```
Inserting 10 menu items...
✅ Added: Pepperoni Classic
✅ Added: Margherita
... (8 more)
🎉 Successfully seeded 10 menu items!
```

### STEP 2: Start Backend Server

**Still in Terminal 1**:
```powershell
uvicorn main:app --reload --port 8000
```

**Wait for**:
```
INFO:     ✅ Application startup complete
```

**Leave this terminal running**! ✅

---

### STEP 3: Frontend Setup (3 min)

**Terminal 2** - Open new PowerShell/CMD:

```powershell
# Navigate to frontend
cd d:\Antigravity\pizza-agent-app\frontend

# Install dependencies (first time only)
npm install
```

**Wait for npm install to complete** (2-3 minutes)

### STEP 4: Start Frontend Server

**Still in Terminal 2**:
```powershell
npm run dev
```

**Wait for**:
```
▲ Next.js 14.1.0
- ready started server on 0.0.0.0:3000
```

**Leave this terminal running**! ✅

---

### STEP 5: Run Automated Tests (2 min)

**Terminal 3** - Open new PowerShell/CMD:

```powershell
# Navigate to project root
cd d:\Antigravity\pizza-agent-app

# Install test dependencies (first time only)
pip install -r test-requirements.txt

# Run all tests
python run-tests.py
```

**Expected Result**:
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

### STEP 6: Manual Browser Testing

**Open Browser**: http://localhost:3000

**Test Pages**:
- [ ] Landing page loads with animations
- [ ] Navigate to `/chat` - send a message
- [ ] Navigate to `/menu` - see pizza grid
- [ ] Search for "cheese" in menu
- [ ] Navigate to `/cart` - see empty state
- [ ] Navigate to `/order` - enter order ID

---

## 🎯 QUICK STATUS CHECK

After each step, verify:

| Step | Check | Status |
|------|-------|--------|
| 1 | `.env` file configured | ⬜ |
| 2 | Backend running on :8000 | ⬜ |
| 3 | Frontend running on :3000 | ⬜ |
| 4 | All 12 tests pass | ⬜ |
| 5 | Browser loads app | ⬜ |

---

## 🐛 TROUBLESHOOTING

### Backend won't start:
```powershell
# Check .env file
notepad backend\.env

# Reinstall dependencies
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend won't start:
```powershell
# Clear cache and reinstall
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Tests fail:
```powershell
# Verify servers are running
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 📊 SUCCESS CRITERIA

✅ All 3 terminals running (backend, frontend, tests completed)  
✅ Tests show: `🎉 All tests passed!`  
✅ Browser loads: http://localhost:3000  
✅ Can send chat messages and receive responses  
✅ Menu displays 10 pizzas  

---

## 🎉 NEXT STEPS AFTER SUCCESS

1. ✅ Test all UI features manually
2. ✅ Review `TESTING-CHECKLIST.md` for detailed tests
3. ✅ Setup monitoring (see `MONITORING.md`)
4. ✅ Deploy to production (see `DEPLOYMENT.md`)

---

**Ready to start?** Open 3 terminals and follow the steps above! 🚀

**Note**: You cannot run these commands from a single terminal. Each server needs its own terminal window to run continuously.
