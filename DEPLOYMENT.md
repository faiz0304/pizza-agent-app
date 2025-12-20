# Deployment Guide - Agentic Pizza Ordering System

Complete deployment instructions for production environments.

## 📋 Prerequisites

- Domain name (optional but recommended)
- MongoDB Atlas account (free tier available)
- HuggingFace account (free API access)
- Twilio account (for WhatsApp)
- Vercel account (for frontend - free tier)
- Render/Railway account (for backend - free tier available)

## 🗄️ Database Setup (MongoDB Atlas)

### 1. Create Cluster
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create free M0 cluster
3. Choose cloud provider and region

### 2. Configure Access
1. **Database Access**: Create user with read/write permissions
2. **Network Access**: Add IP `0.0.0.0/0` (allow from anywhere)

### 3. Get Connection String
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy connection string
4. Replace `<password>` with your actual password

**Example**:
```
mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/pizza_db?retryWrites=true&w=majority
```

### 4. Seed Database
```bash
cd backend
python seed_data.py
```

## 🚀 Backend Deployment (Render)

### Option 1: Web Service (Recommended)

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository

2. **Configure Service**
   - **Name**: `pizza-agent-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

3. **Environment Variables**
   Add all variables from `.env.example`:
   ```
   MONGODB_URI=mongodb+srv://...
   MONGODB_DB_NAME=pizza_db
   HUGGINGFACE_API_TOKEN=hf_...
   TWILIO_ACCOUNT_SID=AC...
   TWILIO_AUTH_TOKEN=...
   TWILIO_WHATSAPP_NUMBER=whatsapp:+...
   FRONTEND_URL=https://your-frontend.vercel.app
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://pizza-agent-backend.onrender.com`

### Option 2: Railway

1. **Create Project**
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure**
   - Add environment variables (same as above)
   - Railway auto-detects Python and installs dependencies

3. **Start Command**
   Add to `railway.json` or set in dashboard:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

## 🌐 Frontend Deployment (Vercel)

### 1. Connect Repository
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository

### 2. Configure Project
- **Framework Preset**: Next.js
- **Root Directory**: `frontend` (if monorepo) or `.` (if separate repo)
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)

### 3. Environment Variables
Add in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://pizza-agent-backend.onrender.com
```

### 4. Deploy
- Click "Deploy"
- Wait for build (2-5 minutes)
- Your app will be live at: `https://your-app.vercel.app`

### 5. Custom Domain (Optional)
1. Go to project settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## 📱 WhatsApp Integration Setup

### 1. Twilio Configuration
1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to "Messaging" → "Try it out" → "Send a WhatsApp message"
3. **For Testing**: Use WhatsApp Sandbox
   - Join sandbox by sending code to +1 415 523 8886
   - Note your sandbox number

4. **For Production** (requires approval):
   - Request WhatsApp Business Profile
   - Get your number approved

### 2. Configure Webhook
1. In Twilio Console, go to "Messaging" → "Settings" → "WhatsApp Sandbox Settings"
2. Set webhook URL:
   ```
   https://pizza-agent-backend.onrender.com/whatsapp/webhook
   ```
3. Method: `POST`
4. Save configuration

### 3. Test WhatsApp
Send message to your Twilio WhatsApp number:
```
Show me the menu
```

You should receive a response from AGENT-X! 🎉

## 🔐 Security Hardening

### Backend
1. **Update CORS**: In `main.py`, replace:
   ```python
   allow_origins=["*"]
   ```
   with:
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```

2. **Environment Variables**: Never commit `.env` files

3. **MongoDB**: Use strong passwords, enable 2FA

### Frontend
1. **API Keys**: Only use `NEXT_PUBLIC_` prefix for client-safe variables
2. **Content Security Policy**: Add CSP headers in `next.config.js`

## 📊 Monitoring

### Backend Logs
- **Render**: Check logs in dashboard
- **Railway**: View logs in project dashboard

### Frontend Analytics
- **Vercel**: Built-in analytics available
- **Alternative**: Add Google Analytics or Plausible

### Database Monitoring
- **MongoDB Atlas**: View metrics in dashboard
- Set up alerts for high usage

## 🔄 Continuous Deployment

### Auto-Deploy on Push
Both Vercel and Render support automatic deployments:
1. Push to `main` branch
2. Services auto-detect changes
3. Rebuild and redeploy automatically

### Branch Previews
- **Vercel**: Auto-creates preview for every PR
- **Render**: Configure preview environments manually

## 🧪 Post-Deployment Testing

### 1. Backend Health Check
```bash
curl https://pizza-agent-backend.onrender.com/health
```

Expected response:
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

### 2. Frontend Test
Visit: `https://your-app.vercel.app`
- Check landing page loads
- Navigate to `/chat`
- Send test message
- Verify response from agent

### 3. WhatsApp Test
Send WhatsApp message:
```
I want a pepperoni pizza
```

Verify agent responds with menu or order creation.

## 🐛 Troubleshooting

### Backend Not Starting
- Check environment variables are set correctly
- Verify MongoDB connection string
- Check Render/Railway logs for errors

### Frontend Can't Connect
- Verify `NEXT_PUBLIC_API_URL` points to backend
- Check CORS settings in backend
- Inspect browser console for errors

### WhatsApp Not Responding
- Verify Twilio webhook URL is correct
- Check Twilio logs for failed requests
- Ensure backend `/whatsapp/webhook` endpoint works

### Database Connection Failed
- Verify MongoDB IP whitelist includes `0.0.0.0/0`
- Check connection string format
- Test connection with MongoDB Compass

## 💰 Cost Estimate

### Free Tier (Development/Testing)
- **MongoDB Atlas**: Free (M0 cluster, 512MB)
- **Render**: Free (750 hours/month)
- **Vercel**: Free (unlimited bandwidth)
- **Twilio Sandbox**: Free for testing
- **HuggingFace**: Free (rate-limited)

**Total**: $0/month ✅

### Production (Paid Tier)
- **MongoDB Atlas**: $9-$57/month (M10-M20)
- **Render**: $7-$25/month (Starter-Standard)
- **Vercel**: $20/month (Pro)
- **Twilio**: ~$0.005/message
- **Groq** (optional): Freemium

**Estimated**: $36-$102/month

## 📝 Maintenance

### Regular Tasks
- Monitor error logs weekly
- Update dependencies monthly
- Check API rate limits
- Review security alerts

### Backup Strategy
- MongoDB: Automated backups (enabled by default)
- Code: Git version control
- Environment Variables: Secure storage (1Password, etc.)

## 🎉 Launch Checklist

- [ ] MongoDB cluster created and seeded
- [ ] Backend deployed to Render/Railway
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] WhatsApp webhook configured
- [ ] CORS settings updated
- [ ] Health checks passing
- [ ] WhatsApp test successful
- [ ] Web chat test successful
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

---

**Congratulations! Your agentic pizza ordering system is now live! 🍕🤖🎉**
