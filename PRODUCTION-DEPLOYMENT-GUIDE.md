# 🚀 Production Deployment Guide
## Agentic Pizza Ordering System

**Time Required**: 20-30 minutes  
**Cost**: FREE (using free tiers)  
**Prerequisites**: GitHub, Vercel, and Render accounts

---

## 📋 Overview

We'll deploy:
- **Frontend** → Vercel (instant, global CDN)
- **Backend** → Render (free tier, auto-deploy)
- **Database** → MongoDB Atlas (already set up)

---

## Step 1: Prepare for Deployment (5 min)

### 1.1 Initialize Git Repository

```powershell
cd d:\Antigravity\pizza-agent-app

# Initialize git (if not done)
git init

# Create .gitignore (already exists)
# Verify .env files are ignored
git status

# Commit everything
git add .
git commit -m "Initial commit - Production ready"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Name: `pizza-agent-app`
3. Make it **Private** (recommended)
4. Don't initialize with README
5. Click "Create repository"

### 1.3 Push to GitHub

```powershell
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/pizza-agent-app.git

# Push code
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (10 min)

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render

### 2.2 Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repo: `pizza-agent-app`
3. Configure:
   - **Name**: `pizza-agent-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 2.3 Add Environment Variables

In Render dashboard,```env
# Backend Environment Variables
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pizza_db
MONGODB_DB_NAME=pizza_db
HUGGINGFACE_API_TOKEN=hf_your_token_here
GROQ_API_KEY=gsk_your_key_here
GOOGLE_API_KEY=AIyour_key_here
TWILIO_ACCOUNT_SID=ACyour_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Note**: We'll update `FRONTEND_URL` after deploying frontend

### 2.4 Deploy

1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. You'll get a URL like: `https://pizza-agent-backend.onrender.com`
4. **Save this URL!**

### 2.5 Test Backend

Visit: `https://pizza-agent-backend.onrender.com/health`

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## Step 3: Deploy Frontend to Vercel (5 min)

### 3.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel

### 3.2 Import Project

1. Click "Add New..." → "Project"
2. Import `pizza-agent-app` from GitHub
3. Configure:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

### 3.3 Add Environment Variables

Add this variable:
```
NEXT_PUBLIC_API_URL=https://pizza-agent-backend.onrender.com
```

**Important**: Use your actual Render backend URL

### 3.4 Deploy

1. Click "Deploy"
2. Wait 2-3 minutes
3. You'll get a URL like: `https://pizza-agent-app.vercel.app`
4. **Save this URL!**

---

## Step 4: Update Backend CORS (2 min)

### 4.1 Update Environment Variable

Go back to Render dashboard:
1. Go to your backend service
2. Environment → Edit
3. Update `FRONTEND_URL` to your Vercel URL:
   ```
   FRONTEND_URL=https://pizza-agent-app.vercel.app
   ```
4. Save changes
5. Render will automatically redeploy

---

## Step 5: Test Production System (5 min)

### 5.1 Test Frontend

Visit: `https://pizza-agent-app.vercel.app`

- ✅ Page loads
- ✅ No errors in console
- ✅ Navigation works

### 5.2 Test Chat

Visit: `https://pizza-agent-app.vercel.app/chat`

- ✅ Type "Hello"
- ✅ Agent responds
- ✅ Try "Show me the menu"

### 5.3 Test Backend

Visit: `https://pizza-agent-backend.onrender.com/docs`

- ✅ API docs load
- ✅ Try /health endpoint
- ✅ Try /menu endpoint

---

## 🎉 Deployment Complete!

### Your Production URLs:

- **Frontend**: https://pizza-agent-app.vercel.app
- **Backend**: https://pizza-agent-backend.onrender.com
- **API Docs**: https://pizza-agent-backend.onrender.com/docs

---

## 🔧 Troubleshooting

### Frontend shows blank page
- Check Vercel deployment logs
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check browser console for errors

### Backend returns 500 errors
- Check Render logs
- Verify environment variables
- Check MongoDB connection

### CORS errors in chat
- Verify `FRONTEND_URL` in Render matches Vercel URL
- Check it has no trailing slash
- Redeploy backend after changing

### Chat doesn't work
- Check Network tab in browser console
- Verify API calls go to correct backend URL
- Check backend /chatbot endpoint in API docs

---

## 📝 Post-Deployment Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Render
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] All pages load correctly
- [ ] Chat works end-to-end
- [ ] Menu displays pizzas
- [ ] No console errors
- [ ] Backend health check returns "healthy"

---

## 🚀 Optional: Custom Domain

### Vercel (Frontend)
1. Go to Project Settings → Domains
2. Add your domain
3. Follow DNS instructions

### Render (Backend)  
1. Go to Settings → Custom Domain
2. Add your domain
3. Follow DNS instructions

---

**Deployment Status**: [ ] Complete / [ ] In Progress  
**Production Ready**: [ ] Yes / [ ] No
