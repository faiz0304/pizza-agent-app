# 🍕 Agentic Pizza Ordering Web App System

A production-grade, full-stack agentic pizza ordering system with autonomous AI assistant, RAG knowledge base, WhatsApp integration, and modern animated UI.
YouTube Demo:
https://youtu.be/cHftjHG2Cz0


LinkedIn Profile:
https://www.linkedin.com/in/faiz-ur-rehman-ashrafi-75b7203a0


## ✨ Features

### Backend
- **🤖 Autonomous Agent (AGENT-X)**: Intelligent decision-making with 7 tools
- **🔍 RAG System**: Semantic search using Chroma vector store with HuggingFace embeddings
- **📱 WhatsApp Integration**: Order via WhatsApp through Twilio webhook
- **🔄 Multi-LLM Support**: HuggingFace, Groq, Google (with automatic fallback)
- **💾 MongoDB Atlas**: Cloud-native database for menu, orders, and customer data
- **🛠️ 7 Agent Tools**:
  - `search_kb`: Knowledge base search
  - `search_menu`: Menu search and filtering
  - `create_order`: Order creation
  - `update_order`: Order modification
  - `order_status`: Order tracking
  - `recommend_pizza`: AI recommendations
  - `ask_llm`: General conversation

### Frontend
- **⚡ Next.js 14**: Modern React framework with App Router
- **🎨 Stunning UI**: Glassmorphism, gradients, animations
- **🔥 Framer Motion**: Smooth transitions and micro-interactions
- **📱 Fully Responsive**: Mobile-first design
- **🎯 Real-time Chat**: Live agent messaging with typing indicators
- **🔎 Smart Search**: Dynamic menu filtering
- **📦 Order Tracking**: Visual timeline with status updates

## 🏗️ Architecture

```
pizza-agent-app/
├── backend/                 # FastAPI Backend
│   ├── agent/              # Agent core & tools registry
│   ├── tools/              # Tool implementations
│   ├── routes/             # API endpoints
│   ├── utils/              # DB, embeddings, LLM client
│   ├── main.py             # FastAPI app
│   └── seed_data.py        # Database seeding
│
└── frontend/               # Next.js Frontend
    ├── app/                # Pages (chat, menu, cart, order)
    ├── components/         # Reusable components
    └── lib/                # API client
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account
- HuggingFace API token
- Twilio account (for WhatsApp)

### Backend Setup

1. **Navigate to backend**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
copy .env.example .env
# Edit .env with your credentials
```

Required env variables:
- `MONGODB_URI`: Your MongoDB Atlas connection string
- `HUGGINGFACE_API_TOKEN`: HuggingFace API key
- `TWILIO_ACCOUNT_SID`: Twilio SID (for WhatsApp)
- `TWILIO_AUTH_TOKEN`: Twilio auth token
- `TWILIO_WHATSAPP_NUMBER`: Your Twilio WhatsApp number

5. **Seed database**:
```bash
python seed_data.py
```

6. **Run server**:
```bash
uvicorn main:app --reload --port 8000
```

Backend will be running at `http://localhost:8000` 🎉

### Frontend Setup

1. **Navigate to frontend**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
```bash
copy .env.local.example .env.local
```

4. **Run development server**:
```bash
npm run dev
```

Frontend will be running at `http://localhost:3000` 🎉

## 📖 Usage

### 1. Web Interface

**Chat with Agent** (`/chat`):
- Type natural language messages
- Ask for recommendations: "I want something spicy"
- Search menu: "Show me vegetarian pizzas"
- Place orders: "Order 2 medium pepperoni pizzas"
- Get support: "What's your refund policy?"

**Browse Menu** (`/menu`):
- View all 10+ pizzas
- Filter by category (veg/non-veg)
- Search by ingredients/tags
- Click "Add to Cart"

**Track Orders** (`/order`):
- Enter order ID
- View real-time status
- See timeline progression

### 2. WhatsApp Integration

**Setup**:
1. Configure Twilio webhook: `https://your-domain.com/whatsapp/webhook`
2. Send message to your Twilio WhatsApp number
3. Chat naturally with AGENT-X

**Example Messages**:
- "Show me your menu"
- "I want a large pepperoni pizza"
- "Track my order ORD-20241204-1234"
- "What are your opening hours?"

### 3. API Usage

**Chatbot Endpoint**:
```bash
curl -X POST http://localhost:8000/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me spicy pizzas",
    "user_id": "test_user"
  }'
```

**Menu Search**:
```bash
curl http://localhost:8000/menu/search?q=cheese
```

**Create Order**:
```bash
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "items": [{
      "menu_id": "pepperoni_classic",
      "name": "Pepperoni Classic",
      "qty": 2,
      "variant": "medium",
      "price": 12.99
    }]
  }'
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB Atlas**: Cloud NoSQL database
- **Chroma DB**: Vector store for RAG
- **HuggingFace**: LLM inference (Mistral-7B)
- **Sentence Transformers**: Embeddings (all-MiniLM-L6-v2)
- **Twilio**: WhatsApp messaging
- **Groq & Google AI**: Optional LLM fallbacks

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Animation library
- **Axios**: HTTP client

## 🐳 Docker Deployment

### Backend
```bash
cd backend
docker build -t pizza-backend .
docker run -p 8000:8000 --env-file .env pizza-backend
```

### Frontend
```bash
cd frontend
docker build -t pizza-frontend .
docker run -p 3000:3000 pizza-frontend
```

## ☁️ Cloud Deployment

### Backend (Render/Railway)
1. Connect GitHub repo
2. Set environment variables
3. Deploy command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Import GitHub repo
2. Set `NEXT_PUBLIC_API_URL` to backend URL
3. Deploy automatically

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8000/health
```

### Frontend Build Test
```bash
cd frontend
npm run build
```

## 📊 Agent System

AGENT-X uses a sophisticated decision-making process:

1. **Message Analysis**: Understands user intent
2. **Tool Selection**: Chooses appropriate tool
3. **Execution**: Calls tool with validated inputs
4. **Response Formation**: Formats user-friendly reply

**System Prompt Template**:
The agent has access to all 7 tools and decides autonomously whether to use them or respond directly.

## 🔐 Security

- Input validation on all endpoints
- Environment variable management
- CORS configuration
- MongoDB connection encryption
- API key rotation support

## 📝 Environment Variables

### Backend (.env)
```env
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=pizza_db
HUGGINGFACE_API_TOKEN=hf_...
GROQ_API_KEY=gsk_... (optional)
GOOGLE_API_KEY=AI... (optional)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### MongoDB Connection Failed
- Verify connection string in `.env`
- Check IP whitelist in MongoDB Atlas
- Ensure network connectivity

### HuggingFace API Errors
- Verify API token is valid
- Check rate limits
- Try fallback providers (Groq/Google)

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS settings in backend `main.py`

### Chroma DB Issues
- Delete `chroma_db/` folder
- Restart backend (auto-reinitializes)

## 📚 Documentation

- **Backend API**: http://localhost:8000/docs (Swagger)
- **Backend README**: `backend/README.md`
- **Implementation Plan**: See planning docs

## 🎯 Future Enhancements

- [ ] User authentication & profiles
- [ ] Payment gateway integration
- [ ] Real-time notifications (WebSockets)
- [ ] Admin dashboard
- [ ] Analytics & reporting
- [ ] Multi-language support
- [ ] Mobile apps (React Native)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

MIT License - feel free to use for commercial or personal projects.

## 🙏 Acknowledgments

- HuggingFace for LLM inference
- MongoDB Atlas for database
- Twilio for WhatsApp integration
- Vercel for frontend hosting
- OpenAI for inspiration

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check troubleshooting section
- Review API documentation

---

**Built with ❤️ and 🍕**

*Powered by AI • Made for Pizza Lovers • Designed for Excellence*
