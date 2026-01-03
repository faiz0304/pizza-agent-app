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
        
        # NEW: Structured session state for token efficiency
        self.session_states: Dict[str, Dict[str, Any]] = {}  # Compressed session state

    
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
        if user_id in self.session_states:
            del self.session_states[user_id]
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
            "expiry_minutes": self.expiry_minutes,
            "active_sessions": len(self.session_states)
        }
    
    # ===== STRUCTURED MEMORY METHODS (NEW) =====
    
    def _extract_entities(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract entities from conversation messages
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Dict with extracted entities (items, quantities, preferences)
        """
        entities = {
            "items": [],
            "quantities": [],
            "preferences": [],
            "mentioned_pizzas": []
        }
        
        # Keywords for entity detection
        size_keywords = ["small", "medium", "large", "personal", "family"]
        preference_keywords = ["veg", "vegetarian", "non-veg", "spicy", "mild", "cheese", "extra cheese", "thin crust", "thick crust"]
        
        for msg in messages:
            content = msg.get("content", "").lower()
            
            # Extract sizes
            for size in size_keywords:
                if size in content:
                    if size not in entities["preferences"]:
                        entities["preferences"].append(size)
            
            # Extract preferences
            for pref in preference_keywords:
                if pref in content:
                    if pref not in entities["preferences"]:
                        entities["preferences"].append(pref)
            
            # Extract quantities (simple number detection)
            import re
            numbers = re.findall(r'\b(\d+)\b', content)
            for num in numbers:
                if 1 <= int(num) <= 10:  # Reasonable quantity range
                    entities["quantities"].append(int(num))
            
            # Extract common pizza names
            pizza_keywords = [
                "pepperoni", "margherita", "veggie", "meat lover", "hawaiian",
                "bbq", "chicken", "supreme", "cheese", "mushroom"
            ]
            for pizza in pizza_keywords:
                if pizza in content:
                    if pizza not in entities["mentioned_pizzas"]:
                        entities["mentioned_pizzas"].append(pizza)
        
        return entities
    
    def _detect_intents(self, messages: List[Dict[str, Any]]) -> List[str]:
        """
        Detect user intents from conversation
        
        Args:
            messages: List of conversation messages
            
        Returns:
            List of detected intents
        """
        intents = []
        
        # Intent keywords mapping
        intent_patterns = {
            "search_menu": ["show", "menu", "options", "what pizzas", "dikhao", "kya hai"],
            "create_order": ["order", "book", "buy", "want", "chahiye", "karo"],
            "order_status": ["track", "status", "where is", "kahan hai"],
            "ask_info": ["hours", "delivery time", "payment", "kitne time"],
            "greeting": ["hi", "hello", "salaam", "hey"],
            "confirmation": ["yes", "haan", "ha", "ok", "confirm", "theek hai"]
        }
        
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "").lower()
                
                for intent, keywords in intent_patterns.items():
                    if any(keyword in content for keyword in keywords):
                        if intent not in intents:
                            intents.append(intent)
        
        return intents
    
    def compress_history(self, user_id: str, last_n: int = 8) -> Dict[str, Any]:
        """
        Compress conversation history into structured session state
        
        Args:
            user_id: User identifier
            last_n: Number of recent messages to analyze
            
        Returns:
            Compressed session state dict
        """
        history = self.get_history(user_id, last_n=last_n)
        
        if not history:
            return {
                "session_id": user_id,
                "recent_intents": [],
                "entities": {},
                "last_action": "none",
                "language_hint": "english",
                "message_count": 0
            }
        
        # Extract structured data
        intents = self._detect_intents(history)
        entities = self._extract_entities(history)
        
        # Detect language hint
        last_user_msg = next(
            (msg["content"] for msg in reversed(history) if msg.get("role") == "user"),
            ""
        )
        language_hint = self._detect_language_hint(last_user_msg)
        
        # Determine last action
        last_action = "conversation"
        if "confirmation" in intents:
            last_action = "confirming_order"
        elif "create_order" in intents:
            last_action = "order_requested"
        elif "search_menu" in intents:
            last_action = "browsing_menu"
        
        # Create compressed state
        compressed_state = {
            "session_id": user_id,
            "recent_intents": intents[-3:] if len(intents) > 3 else intents,  # Keep last 3 intents
            "entities": entities,
            "last_action": last_action,
            "language_hint": language_hint,
            "message_count": len(history),
            "has_pending_order": user_id in self.pending_orders
        }
        
        # Store in session state
        self.session_states[user_id] = compressed_state
        
        logger.debug(f"Compressed session for {user_id}: {compressed_state}")
        
        return compressed_state
    
    def _detect_language_hint(self, text: str) -> str:
        """Detect language from text (simple heuristic)"""
        text_lower = text.lower()
        
        # Roman Urdu/Hindi indicators
        urdu_hindi_keywords = [
            "kya", "hai", "haan", "nahi", "acha", "theek", "kitne",
            "kahan", "kab", "kaise", "chahiye", "dikhao", "batao",
            "karo", "krdo", "mujhe", "apna", "bhi"
        ]
        
        if any(keyword in text_lower for keyword in urdu_hindi_keywords):
            return "roman_urdu"
        
        return "english"
    
    def get_context_for_prompt(self, user_id: str, include_raw_history: bool = False) -> str:
        """
        Get optimized context for LLM prompt (token-efficient)
        
        Args:
            user_id: User identifier
            include_raw_history: If True, include recent raw messages along with structured state
            
        Returns:
            Formatted context string for prompt
        """
        # Get or create compressed state
        if user_id not in self.session_states:
            self.compress_history(user_id)
        
        state = self.session_states.get(user_id, {})
        
        # Build compact context
        context_parts = []
        
        # Add session info
        if state.get("message_count", 0) > 0:
            context_parts.append(f"Session: {state.get('message_count')} messages exchanged")
        
        # Add language hint
        if state.get("language_hint") != "english":
            context_parts.append(f"Language: {state.get('language_hint')}")
        
        # Add recent intents
        if state.get("recent_intents"):
            intents_str = ", ".join(state["recent_intents"])
            context_parts.append(f"Recent intents: {intents_str}")
        
        # Add entities
        entities = state.get("entities", {})
        if entities.get("mentioned_pizzas"):
            pizzas = ", ".join(entities["mentioned_pizzas"][:3])  # Limit to 3
            context_parts.append(f"Pizzas mentioned: {pizzas}")
        
        if entities.get("preferences"):
            prefs = ", ".join(entities["preferences"][:3])  # Limit to 3
            context_parts.append(f"Preferences: {prefs}")
        
        # Add pending order status
        if state.get("has_pending_order"):
            pending = self.get_pending_order(user_id)
            if pending:
                items = pending.get("items", [])
                if items:
                    item_summary = f"{len(items)} item(s)"
                    context_parts.append(f"⚠️ PENDING ORDER: {item_summary} awaiting confirmation")
        
        # Add last action
        if state.get("last_action") and state["last_action"] != "none":
            context_parts.append(f"Last action: {state['last_action']}")
        
        # Combine into compact format
        if not context_parts:
            return ""
        
        compact_context = "📋 Session Context:\n" + "\n".join(f"• {part}" for part in context_parts)
        
        # Optionally include recent raw messages (for critical context)
        if include_raw_history:
            recent = self.get_history(user_id, last_n=3)
            if recent:
                compact_context += "\n\n💬 Recent Messages:\n"
                for msg in recent:
                    role = "User" if msg["role"] == "user" else "Bot"
                    content = msg["content"][:80]  # Truncate
                    compact_context += f"{role}: {content}\n"
        
        return compact_context
    
    def update_session_state(self, user_id: str, **updates):
        """
        Update specific fields in session state
        
        Args:
            user_id: User identifier
            **updates: Key-value pairs to update
        """
        if user_id not in self.session_states:
            self.session_states[user_id] = {
                "session_id": user_id,
                "recent_intents": [],
                "entities": {},
                "last_action": "none",
                "language_hint": "english"
            }
        
        self.session_states[user_id].update(updates)
        logger.debug(f"Updated session state for {user_id}: {updates}")



# Global memory instance
conversation_memory = ConversationMemory()


def get_conversation_memory() -> ConversationMemory:
    """Get the global conversation memory instance"""
    return conversation_memory
