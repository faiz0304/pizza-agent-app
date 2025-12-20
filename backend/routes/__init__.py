"""Routes package initialization"""
from .chatbot import router as chatbot_router
from .menu import router as menu_router
from .order import router as order_router
from .whatsapp import router as whatsapp_router

__all__ = [
    "chatbot_router",
    "menu_router",
    "order_router",
    "whatsapp_router"
]
