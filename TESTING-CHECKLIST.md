# Quick Testing Checklist
# Agentic Pizza Ordering System

## ⚡ Quick Setup
- [ ] MongoDB running (local or Atlas connected)
- [ ] Backend server started on port 8000
- [ ] Frontend server started on port 3000
- [ ] Database seeded with menu items

## 🔧 Backend (5 min)
- [ ] Health check: `GET /health` → 200 OK
- [ ] Menu list: `GET /menu` → 10 items
- [ ] Menu search: `GET /menu/search?q=spicy` → filtered results
- [ ] Chatbot hello: `POST /chatbot {"message": "Hello"}` → greeting
- [ ] Chatbot search: `POST /chatbot {"message": "Show pizzas"}` → tool: search_menu
- [ ] Chatbot KB: `POST /chatbot {"message": "refund policy"}` → tool: search_kb

## 🌐 Frontend (5 min)
- [ ] Landing page loads with animations
- [ ] Navigation menu works (all links)
- [ ] Chat page: can send/receive messages
- [ ] Chat page: typing indicator shows
- [ ] Chat page: tool badges display
- [ ] Menu page: grid displays 10 pizzas
- [ ] Menu page: category filters work
- [ ] Menu page: search box filters
- [ ] Cart page: shows empty state
- [ ] Order page: input and track button work

## 🔗 Integration (3 min)
- [ ] Frontend connects to backend (no CORS errors)
- [ ] Chat messages reach agent
- [ ] Agent selects correct tools
- [ ] Responses display properly
- [ ] Error handling works

## 📱 WhatsApp (Optional, 5 min)
- [ ] Webhook configured in Twilio
- [ ] Send "Show menu" → receives list
- [ ] Send "Refund policy" → receives KB response
- [ ] Clean formatting (no JSON/markdown)
- [ ] Returns 200 OK to Twilio

## ✅ Success Criteria
- [ ] All tests pass
- [ ] No console errors
- [ ] Response time < 5s
- [ ] Animations smooth
- [ ] Mobile responsive

## 🚀 Automated Testing
```bash
# Bash (Linux/Mac)
./run-tests.sh

# Python (Cross-platform)
python run-tests.py

# expected: All tests pass ✅
```

## 📊 Performance Check
- [ ] Backend memory < 500MB
- [ ] Frontend memory < 200MB
- [ ] Page load < 3s
- [ ] API response < 2s

## 🐛 Common Fixes
| Issue | Fix |
|-------|-----|
| Connection refused | Start server |
| MongoDB error | Check .env connection string |
| CORS error | Verify ALLOWED_ORIGINS |
| HF API error | Check token in .env |
| Chroma error | Delete chroma_db/ folder |

---

**Total Time**: ~15 minutes  
**Status**: Ready for production ✅
