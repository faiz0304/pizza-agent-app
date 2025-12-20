# Agentic Pizza Ordering System - Backend

Production-grade FastAPI backend with autonomous agent, RAG system, and WhatsApp integration.

## 🚀 Features

- **Autonomous Agent (AGENT-X)**: Intelligent pizza ordering assistant with tool-using capabilities
- **RAG System**: Knowledge base search using Chroma vector store
- **7 Agent Tools**: search_kb, search_menu, create_order, update_order, order_status, recommend_pizza, ask_llm
- **Multi-LLM Support**: HuggingFace (primary), Groq, Google (fallbacks)
- **WhatsApp Integration**: Twilio webhook for WhatsApp messaging
- **MongoDB Atlas**: Cloud database for menu, orders, and users
- **RESTful API**: Comprehensive endpoints for all operations

## 📋 Prerequisites

- Python 3.10+
- MongoDB Atlas account (or local MongoDB)
- HuggingFace API token
- Twilio account (for WhatsApp integration)
- Optional: Groq API key, Google API key

## ⚙️ Installation

### 1. Clone and Navigate
```bash
cd d:\Antigravity\pizza-agent-app\backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Copy `.env.example` to `.env` and fill in your credentials:

```bash
copy .env.example .env
```

**Required variables**:
```env
# MongoDB
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=pizza_db

# HuggingFace
HUGGINGFACE_API_TOKEN=your_hf_token

# Twilio 
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 5. Seed Database
```bash
python seed_data.py
```

This will populate the menu collection with 10 sample pizzas.

## 🏃 Running the Server

### Development Mode
```bash
uvicorn main:app --reload --port 8000
```

### Production Mode
```bash
python main.py
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Chatbot
- `POST /chatbot` - Main agent interaction endpoint

**Request**:
```json
{
  "message": "I want a spicy pizza",
  "user_id": "user_123",
  "conversation_history": []
}
```

**Response**:
```json
{
  "reply": "🍕 Found 2 spicy pizzas: ...",
  "tool_used": "search_menu",
  "status": "success"
}
```

#### Menu
- `GET /menu` - List all menu items
- `GET /menu/search?q=spicy` - Search menu
- `GET /menu/{item_id}` - Get specific item

#### Orders
- `POST /order` - Create order
- `GET /order/{order_id}` - Get order status
- `PUT /order/{order_id}` - Update order

#### WhatsApp
- `POST /whatsapp/webhook` - Twilio webhook (configured in Twilio dashboard)
- `GET /whatsapp/status` - Check integration status

## 🤖 Agent System

The autonomous agent (`AGENT-X`) analyzes user messages and decides whether to:
1. Call a tool (search, order, recommend)
2. Respond directly

**Agent Flow**:
```
User Message → Agent Reasoning → Tool Selection → Tool Execution → Formatted Response
```

### Available Tools

| Tool | Description | Example Use |
|------|-------------|-------------|
| `search_kb` | Search knowledge base | "What's your refund policy?" |
| `search_menu` | Find pizzas | "Show me vegetarian options" |
| `create_order` | Place an order | "Order 2 medium pepperoni" |
| `update_order` | Modify order | "Change to large size" |
| `order_status` | Check order | "Where is my order?" |
| `recommend_pizza` | Get recommendations | "I want something cheesy" |
| `ask_llm` | General conversation | "How are you?" |

## 🔧 Project Structure

```
backend/
├── agent/
│   ├── agent.py              # Core agent with decision logic
│   └── tools_registry.py     # Tool registration & execution
├── tools/
│   ├── rag_tool.py           # Knowledge base search (Chroma)
│   ├── menu_tool.py          # Menu search & filtering
│   ├── order_tool.py         # Order CRUD operations
│   └── recommend_tool.py     # AI recommendations
├── routes/
│   ├── chatbot.py            # POST /chatbot
│   ├── menu.py               # GET /menu, /menu/search
│   ├── order.py              # POST/GET /order
│   └── whatsapp.py           # POST /whatsapp/webhook
├── utils/
│   ├── db.py                 # MongoDB connection & queries
│   ├── embeddings.py         # Sentence transformers
│   └── hf_client.py          # Multi-LLM client
├── main.py                   # FastAPI app entry point
├── seed_data.py              # Database seeding script
├── requirements.txt
└── Dockerfile
```

## 🧪 Testing

Run the chatbot endpoint:
```bash
curl -X POST http://localhost:8000/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all pizzas", "user_id": "test_user"}'
```

Test menu search:
```bash
curl http://localhost:8000/menu/search?q=cheese
```

## 🐳 Docker Deployment

Build image:
```bash
docker build -t pizza-backend .
```

Run container:
```bash
docker run -p 8000:8000 --env-file .env pizza-backend
```

## 📱 WhatsApp Setup

1. Create Twilio account: https://www.twilio.com/try-twilio
2. Setup WhatsApp sandbox or get approved number
3. Configure webhook URL in Twilio console:
   - Webhook URL: `https://your-domain.com/whatsapp/webhook`
   - Method: POST
4. Test by sending a WhatsApp message to your Twilio number

## 🔍 Troubleshooting

### MongoDB Connection Failed
- Check `MONGODB_URI` in `.env`
- Verify IP whitelist in MongoDB Atlas
- Test connection with MongoDB Compass

### HuggingFace API Errors
- Verify `HUGGINGFACE_API_TOKEN` is valid
- Check rate limits
- Try fallback providers (Groq, Google)

### Chroma DB Issues
- Delete `chroma_db` folder and restart
- Knowledge base will reinitialize automatically

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## 📊 Monitoring

Check health:
```bash
curl http://localhost:8000/health
```

Response:
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

## 🛠️ Development

### Adding a New Tool

1. Create tool file in `tools/`:
```python
def my_new_tool(param: str) -> dict:
    # Implementation
    return {"result": "success"}
```

2. Register in `agent/tools_registry.py`:
```python
self.register_tool(
    name="my_new_tool",
    function=my_new_tool,
    description="What this tool does"
)
```

3. Update agent system prompt in `agent/agent.py` to include the new tool

## 📝 License

MIT License

## 🤝 Support

For issues or questions, please check the main project README or create an issue.

---

**Built with**: FastAPI, MongoDB, Chroma, HuggingFace, Twilio
