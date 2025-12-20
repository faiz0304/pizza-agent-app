"""
FastAPI Main Application
Agentic Pizza Ordering System Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from routes import chatbot_router, menu_router, order_router, whatsapp_router
from utils.db import get_db
from tools.rag_tool import initialize_knowledge_base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    Handles startup and shutdown
    """
    # Startup
    logger.info("🚀 Starting Agentic Pizza Ordering System...")
    
    # Connect to database
    db = get_db()
    if not db.connect():
        logger.error("Failed to connect to MongoDB")
    
    # Initialize knowledge base
    try:
        initialize_knowledge_base()
        logger.info("✅ Knowledge base initialized")
    except Exception as e:
        logger.warning(f"Knowledge base initialization warning: {e}")
    
    logger.info("✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    db.disconnect()
    logger.info("✅ Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Agentic Pizza Ordering System",
    description="AI-powered pizza ordering system with RAG, autonomous agent, and WhatsApp integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]

# Add production frontend URL if set
if FRONTEND_URL and FRONTEND_URL not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chatbot_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(whatsapp_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Agentic Pizza Ordering System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chatbot": "/chatbot",
            "menu": "/menu",
            "orders": "/order",
            "whatsapp": "/whatsapp",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check database connection
    db = get_db()
    db_status = "connected" if db.db is not None else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "services": {
            "chatbot": "active",
            "menu": "active",
            "orders": "active",
            "whatsapp": "active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
