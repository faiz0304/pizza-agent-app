# Testing Guide - Agentic Pizza Ordering System

## 🔧 Pre-Testing Setup

### 1. Start MongoDB
If using local MongoDB:
```bash
mongod --dbpath=/path/to/data
```

If using MongoDB Atlas:
- Ensure connection string is in `.env`
- Verify IP whitelist includes your IP

### 2. Start Backend Server

```bash
cd d:\Antigravity\pizza-agent-app\backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Seed database (first time only)
python seed_data.py

# Start server
uvicorn main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     🚀 Starting Agentic Pizza Ordering System...
INFO:     ✅ Connected to MongoDB: pizza_db
INFO:     ✅ Knowledge base initialized
INFO:     ✅ Application startup complete
```

### 3. Start Frontend Server

```bash
cd d:\Antigravity\pizza-agent-app\frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected Output**:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- info  Loaded env from .env.local
```

---

## ✅ Backend Testing

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "services": {
    "chatbot": "active",
    "menu": "active",
    "orders": "active",
    "whatsapp": "active"
  }
}
```

### Test 2: Menu Listing
```bash
curl http://localhost:8000/menu
```

**Expected**: JSON array with 10 pizza items

### Test 3: Menu Search
```bash
curl "http://localhost:8000/menu/search?q=spicy"
```

**Expected**: Filtered list with spicy pizzas

### Test 4: Chatbot (Simple Query)
```bash
curl -X POST http://localhost:8000/chatbot \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello\", \"user_id\": \"test_user\"}"
```

**Expected Response**:
```json
{
  "reply": "Hello! I'm doing great...",
  "tool_used": null,
  "status": "success"
}
```

### Test 5: Chatbot (Search Menu)
```bash
curl -X POST http://localhost:8000/chatbot \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Show me spicy pizzas\", \"user_id\": \"test_user\"}"
```

**Expected**: Agent uses `search_menu` tool and returns formatted list

### Test 6: Chatbot (KB Search)
```bash
curl -X POST http://localhost:8000/chatbot \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is your refund policy?\", \"user_id\": \"test_user\"}"
```

**Expected**: Agent uses `search_kb` tool and returns policy info

---

## 🌐 Frontend Testing

### Test 1: Landing Page
1. Navigate to: `http://localhost:3000`
2. Verify:
   - Hero section loads with animations
   - "Welcome to AGENT-X Pizza" title visible
   - Feature cards (AI Assistant, Fast & Smart, Multi-Channel)
   - Stats section (10+ Pizzas, 24/7 Support, etc.)
   - Navigation menu works

### Test 2: Chat Page
1. Navigate to: `http://localhost:3000/chat`
2. Test messages:

**Message 1**: "Show me all pizzas"
- Expected: List of pizzas from search_menu tool
- Verify: Tool badge shows "search_menu"

**Message 2**: "I want something spicy and cheesy"
- Expected: Recommendations from recommend_pizza tool
- Verify: 3 pizza suggestions with reasons

**Message 3**: "What are your delivery hours?"
- Expected: KB response about opening hours
- Verify: Tool badge shows "search_kb"

**Message 4**: "How are you?"
- Expected: Direct casual reply (no tool)
- Verify: No tool badge

3. Verify:
   - Typing indicator appears while waiting
   - Messages have smooth entrance animations
   - Auto-scroll to latest message
   - Quick action buttons work

### Test 3: Menu Page
1. Navigate to: `http://localhost:3000/menu`
2. Verify:
   - Grid displays 10 pizzas
   - Category filters work (All, Veg, Non-Veg)
   - Search box filters results
   - Pizza cards show:
     - Name & price
     - Tags (popular, spicy, etc.)
     - Description
     - Ingredients
     - "Add to Cart" button

3. Test search: "cheese"
   - Verify: Only cheese pizzas shown

4. Test filter: Click "Vegetarian"
   - Verify: Only veg pizzas shown

### Test 4: Cart Page
1. Navigate to: `http://localhost:3000/cart`
2. Verify:
   - Empty state shows
   - "Browse Menu" button navigates to /menu

### Test 5: Order Tracking
1. Navigate to: `http://localhost:3000/order`
2. Enter order ID: `ORD-20241204-1234` (will fail - expected)
3. Verify:
   - "Order not found" error message
   - Input field and Track button work

---

## 📱 WhatsApp Testing

### Setup
1. Configure Twilio webhook:
   ```
   https://your-backend-url.com/whatsapp/webhook
   ```

2. Join WhatsApp sandbox (if testing):
   - Send code to +1 415 523 8886

### Test Messages

**Test 1**: "Show me the menu"
- Expected: List of pizzas
- Verify: No JSON/markdown artifacts in WhatsApp

**Test 2**: "I want a large pepperoni pizza"
- Expected: Agent offers to create order
- Verify: Clean formatting

**Test 3**: "What's your refund policy?"
- Expected: KB response about refunds
- Verify: Readable in WhatsApp

**Test 4**: "Track order ORD-123"
- Expected: Order status or "not found"
- Verify: Response received

### Check Twilio Logs
- Verify webhook receives 200 OK immediately
- Check no retry attempts
- Verify message delivery status

---

## 🐛 Common Issues & Fixes

### Issue 1: "Connection Refused"
**Cause**: Server not running
**Fix**: Start backend/frontend servers

### Issue 2: MongoDB Connection Error
**Cause**: Invalid connection string or network issue
**Fix**: 
- Check `MONGODB_URI` in `.env`
- Verify IP whitelist in MongoDB Atlas
- Test connection with MongoDB Compass

### Issue 3: HuggingFace API Error
**Cause**: Invalid token or rate limit
**Fix**:
- Verify `HUGGINGFACE_API_TOKEN` in `.env`
- Check HuggingFace dashboard for limits
- Try Groq fallback

### Issue 4: Agent Returns Raw JSON
**Cause**: LLM not following format
**Fix**: Already handled with robust JSON parsing fallback

### Issue 5: CORS Error in Browser
**Cause**: Frontend URL not in allowed origins
**Fix**: Add frontend URL to `ALLOWED_ORIGINS` in `main.py`

### Issue 6: WhatsApp Webhook Timeout
**Cause**: Slow response
**Fix**: Already fixed - returns 200 OK immediately

### Issue 7: Chroma DB Error
**Cause**: Permissions or corrupt database
**Fix**: Delete `chroma_db/` folder and restart backend

---

## 📊 Testing Checklist

### Backend ✅
- [ ] Health endpoint returns 200
- [ ] Menu listing works
- [ ] Menu search returns results
- [ ] Chatbot responds to simple greeting
- [ ] Agent selects correct tools
- [ ] search_kb tool works
- [ ] search_menu tool works
- [ ] recommend_pizza tool works
- [ ] RAG vector search returns results
- [ ] MongoDB queries execute
- [ ] Chroma initialized properly

### Frontend ✅
- [ ] Landing page loads with animations
- [ ] Navigation menu works
- [ ] Chat page loads
- [ ] Can send messages
- [ ] Receives agent responses
- [ ] Typing indicator shows
- [ ] Tool badges display correctly
- [ ] Menu page displays grid
- [ ] Search functionality works
- [ ] Category filters work
- [ ] Hover animations smooth
- [ ] Cart page shows empty state
- [ ] Order tracking input works
- [ ] Responsive on mobile

### Integration ✅
- [ ] Frontend connects to backend
- [ ] Chat messages reach agent
- [ ] Agent responses display correctly
- [ ] Tool calls execute successfully
- [ ] Error messages show properly
- [ ] No CORS errors
- [ ] API calls succeed

### WhatsApp (Optional) ✅
- [ ] Webhook configured
- [ ] Receives messages
- [ ] Sends responses
- [ ] Returns 200 OK immediately
- [ ] No timeout errors
- [ ] Clean formatting (no JSON/markdown)
- [ ] Idempotency handling works

---

## 🚀 Performance Testing

### Load Test Backend
```bash
# Install Apache Bench
# Test chatbot endpoint
ab -n 100 -c 10 -p message.json -T application/json http://localhost:8000/chatbot
```

message.json:
```json
{"message": "Hello", "user_id": "test"}
```

**Expected**: 100% success rate, <1s average response time

### Monitor Memory
```bash
# Backend memory usage
ps aux | grep uvicorn

# Frontend memory usage
ps aux | grep node
```

---

## 📝 Success Criteria

✅ **All tests pass**
✅ **No console errors**
✅ **Animations smooth (60fps)**
✅ **Agent selects correct tools**
✅ **Response time < 5 seconds**
✅ **WhatsApp delivers messages**
✅ **Mobile responsive**
✅ **No memory leaks**

---

## 🎯 Next Steps After Testing

1. Fix any identified issues
2. Optimize slow queries
3. Add error tracking (Sentry)
4. Setup monitoring (Prometheus)
5. Deploy to staging
6. User acceptance testing
7. Production deployment

---

**Happy Testing! 🍕🤖**
