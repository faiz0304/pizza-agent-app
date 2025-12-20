"""
Conversation Memory Manager
Handles short-term conversation context for improved customer service
"""
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Manages conversation history and context for each user
    Provides short-term memory for better contextual responses
    """
    
    def __init__(self, max_history: int = 10, expiry_minutes: int = 30):
        """
        Initialize conversation memory
        
        Args:
            max_history: Maximum number of messages to keep per user
            expiry_minutes: Minutes after which conversation expires
        """
        self.max_history = max_history
        self.expiry_minutes = expiry_minutes
        self.conversations: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.last_activity: Dict[str, datetime] = {}
        self.pending_orders: Dict[str, Dict[str, Any]] = {}  # Track pending orders awaiting confirmation
    
    def add_message(self, user_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a message to conversation history
        
        Args:
            user_id: User identifier
            role: Message role (user/assistant)
            content: Message content
            metadata: Optional metadata dict
        """
        # Clean expired conversations first
        self._clean_expired()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        }
        
        # Add message
        self.conversations[user_id].append(message)
        
        # Trim to max history
        if len(self.conversations[user_id]) > self.max_history:
            self.conversations[user_id] = self.conversations[user_id][-self.max_history:]
        
        # Update last activity
        self.last_activity[user_id] = datetime.utcnow()
        
        logger.debug(f"Added message for user {user_id}: {role} - {content[:50]}...")
    
    def set_pending_order(self, user_id: str, order_details: Dict[str, Any]):
        """Store a pending order awaiting confirmation"""
        self.pending_orders[user_id] = order_details
        logger.info(f"Pending order set for user {user_id}: {order_details}")
    
    def get_pending_order(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get pending order for user"""
        return self.pending_orders.get(user_id)
    
    def clear_pending_order(self, user_id: str):
        """Clear pending order after confirmation or cancellation"""
        if user_id in self.pending_orders:
            del self.pending_orders[user_id]
            logger.info(f"Cleared pending order for user {user_id}")
    
    def get_history(self, user_id: str, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history for a user
        
        Args:
            user_id: User identifier
            last_n: Optional number of recent messages to return
            
        Returns:
            List of message dicts
        """
        # Clean expired first
        self._clean_expired()
        
        history = self.conversations.get(user_id, [])
        
        if last_n:
            return history[-last_n:]
        return history
    
    def get_context_summary(self, user_id: str) -> str:
        """
        Get a formatted summary of recent conversation context
        
        Args:
            user_id: User identifier
            
        Returns:
            Formatted context string
        """
        history = self.get_history(user_id, last_n=5)
        
        if not history:
            return "No previous conversation"
        
        # Format recent conversation
        context_lines = []
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:100]  # Truncate long messages
            context_lines.append(f"{role}: {content}")
        
        return "\n".join(context_lines)
    
    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]
        if user_id in self.last_activity:
            del self.last_activity[user_id]
        logger.info(f"Cleared conversation history for user {user_id}")
    
    def _clean_expired(self):
        """Remove expired conversations"""
        now = datetime.utcnow()
        expired_users = []
        
        for user_id, last_active in self.last_activity.items():
            if now - last_active > timedelta(minutes=self.expiry_minutes):
                expired_users.append(user_id)
        
        for user_id in expired_users:
            self.clear_history(user_id)
            logger.debug(f"Expired conversation for user {user_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "active_conversations": len(self.conversations),
            "total_messages": sum(len(msgs) for msgs in self.conversations.values()),
            "max_history": self.max_history,
            "expiry_minutes": self.expiry_minutes
        }


# Global memory instance
conversation_memory = ConversationMemory()


def get_conversation_memory() -> ConversationMemory:
    """Get the global conversation memory instance"""
    return conversation_memory
