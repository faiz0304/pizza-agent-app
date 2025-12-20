# 🔐 Secrets Setup Guide

This guide will help you configure all the necessary API keys and secrets to run the Pizza Agent App.

## 📋 Overview

The application requires several external services and API keys:
- **MongoDB Atlas** - Database storage
- **HuggingFace** - Primary LLM provider
- **Twilio** - WhatsApp integration
- **Groq** (Optional) - Fallback LLM
- **Google AI** (Optional) - Fallback LLM

---

## 🚀 Quick Setup Steps

### 1. Backend Environment Variables

**Location:** `backend/.env`

```bash
# Navigate to backend folder
cd backend

# Copy the example file
copy .env.example .env

# Edit .env with your actual values
notepad .env  # Windows
# or
nano .env     # Mac/Linux
```

### 2. Frontend Environment Variables

**Location:** `frontend/.env.local`

```bash
# Navigate to frontend folder
cd frontend

# Copy the example file
copy .env.local.example .env.local

# Edit .env.local with your backend URL
notepad .env.local  # Windows
```

---

## 📝 Detailed Service Setup

### 🗄️ MongoDB Atlas (Required)

**Purpose:** Database for menu, orders, and customer data

**Steps:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Create a new cluster (free tier is fine)
4. Click "Connect" → "Connect your application"
5. Copy the connection string
6. Replace `<password>` with your database password
7. Add to `backend/.env`:
   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   MONGODB_DB_NAME=pizza_db
   ```

**Additional Steps:**
- In MongoDB Atlas, go to Network Access
- Add your IP address to whitelist (or use `0.0.0.0/0` for all IPs during development)

---

### 🤖 HuggingFace API (Required)

**Purpose:** Primary LLM for the AI agent

**Steps:**
1. Go to [HuggingFace](https://huggingface.co)
2. Sign up for an account
3. Go to Settings → [Access Tokens](https://huggingface.co/settings/tokens)
4. Click "New token"
5. Select "Read" permission
6. Copy the token (starts with `hf_`)
7. Add to `backend/.env`:
   ```env
   HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Free Tier:** HuggingFace offers a generous free tier for inference API calls.

---

### 📱 Twilio WhatsApp (Required for WhatsApp Features)

**Purpose:** Send and receive WhatsApp messages

**Steps:**
1. Go to [Twilio](https://www.twilio.com)
2. Sign up for an account (free trial available with $15 credit)
3. Go to Console Dashboard
4. Copy your **Account SID** and **Auth Token**
5. For WhatsApp:
   - Go to Messaging → Try it out → Send a WhatsApp message
   - Join the sandbox by sending the code to the provided number
   - Use the sandbox number: `whatsapp:+14155238886`
6. Add to `backend/.env`:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

**Production WhatsApp:**
- For production, you'll need to get WhatsApp Business API approval
- This requires a business profile and verification

**Webhook Configuration:**
- In Twilio Console → Messaging → Settings → WhatsApp Sandbox
- Set webhook URL to: `https://your-backend-url.com/whatsapp/webhook`
- Select "HTTP POST" method

---

### ⚡ Groq API (Optional - Recommended)

**Purpose:** Fast fallback LLM provider

**Steps:**
1. Go to [Groq Console](https://console.groq.com)
2. Sign up for an account
3. Go to API Keys
4. Create new API key
5. Copy the key (starts with `gsk_`)
6. Add to `backend/.env`:
   ```env
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Benefits:** Groq provides extremely fast inference speeds and is a good fallback if HuggingFace is slow or unavailable.

---

### 🔍 Google AI (Optional)

**Purpose:** Additional fallback LLM provider

**Steps:**
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Sign in with Google account
3. Click "Get API key"
4. Create new API key
5. Copy the key (starts with `AI`)
6. Add to `backend/.env`:
   ```env
   GOOGLE_API_KEY=AIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Free Tier:** Google AI offers free tier with rate limits.

---

## 🔐 Security Best Practices

### ✅ DO:
- ✅ Keep `.env` and `.env.local` files private
- ✅ Use different API keys for development and production
- ✅ Rotate API keys regularly
- ✅ Use environment-specific keys
- ✅ Store production secrets in secure secret managers

### ❌ DON'T:
- ❌ Never commit `.env` files to Git
- ❌ Never share API keys publicly
- ❌ Never hardcode secrets in code
- ❌ Never use production keys in development

---

## 📊 Configuration Checklist

Use this checklist to ensure everything is configured:

### Backend Configuration
- [ ] `MONGODB_URI` - MongoDB Atlas connection string
- [ ] `MONGODB_DB_NAME` - Database name (pizza_db)
- [ ] `HUGGINGFACE_API_TOKEN` - HuggingFace API token
- [ ] `TWILIO_ACCOUNT_SID` - Twilio Account SID
- [ ] `TWILIO_AUTH_TOKEN` - Twilio Auth Token
- [ ] `TWILIO_WHATSAPP_NUMBER` - Twilio WhatsApp number
- [ ] `FRONTEND_URL` - Frontend URL for CORS
- [ ] Optional: `GROQ_API_KEY` - Groq API key
- [ ] Optional: `GOOGLE_API_KEY` - Google AI key

### Frontend Configuration
- [ ] `NEXT_PUBLIC_API_URL` - Backend API URL

### Database Setup
- [ ] MongoDB cluster created
- [ ] IP address whitelisted in MongoDB Atlas
- [ ] Database seeded with initial data (`python backend/seed_data.py`)

### Twilio Setup (if using WhatsApp)
- [ ] Twilio account created
- [ ] WhatsApp sandbox joined
- [ ] Webhook configured (for production)

---

## 🧪 Testing Your Configuration

### Backend Test:
```bash
cd backend
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Test MongoDB connection
python -c "from utils.db import get_db; db=get_db(); print('✓ MongoDB connected' if db.connect() else '✗ MongoDB failed')"

# Test ChromaDB
python -c "import chromadb; print('✓ ChromaDB working')"

# Start backend
python main.py
# Should start without errors on http://localhost:8000
```

### Frontend Test:
```bash
cd frontend

# Start frontend
npm run dev
# Should start on http://localhost:3000
```

### Integration Test:
1. Open http://localhost:3000
2. Go to Chat page
3. Send a message: "Show me your menu"
4. Should receive response from agent

---

## ❓ Troubleshooting

### MongoDB Connection Failed
- Verify connection string is correct
- Check IP whitelist in MongoDB Atlas
- Ensure password doesn't contain special characters (URL encode if needed)

### HuggingFace API Errors
- Verify token is valid
- Check rate limits
- Try using Groq or Google AI as fallback

### Twilio WhatsApp Not Working
- Verify Account SID and Auth Token
- Check webhook URL is correct and accessible
- Ensure WhatsApp sandbox is joined

### Frontend Can't Connect to Backend
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Check CORS settings in backend `main.py`

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section in [workflow.txt](./workflow.txt)
2. Review API documentation for each service
3. Check server logs for error messages
4. Verify all environment variables are set correctly

---

## 🔄 Environment Variable Updates

When adding new environment variables:
1. Add to `.env.example` (never `.env`)
2. Document in this guide
3. Update README.md if needed
4. Notify team members to update their local `.env` files

---

**Remember:** Security is crucial! Never commit secrets to version control.

🔒 **Keep your secrets secret!** 🔒
