"""
Pydantic Models for Memory System
Defines schemas for long-term user preferences and behavior patterns
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime


class UserPreferences(BaseModel):
    """
    Long-term user preference storage model
    Stores high-signal information about user behavior and preferences
    """
    user_id: str = Field(..., description="Unique user identifier")
    whatsapp_number: Optional[str] = Field(None, description="WhatsApp number for  WhatsApp users")
    
    # Preferences
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="User preferences including favorites, diet type, etc."
    )
    
    # Behavior patterns
    behavior_patterns: Dict[str, Any] = Field(
        default_factory=dict,
        description="Learned behavior patterns like order time, avg value"
    )
    
    # Language preference
    language_preference: str = Field(
        default="english",
        description="Detected language preference (english, roman_urdu, roman_hindi)"
    )
    
    # Last successful order
    last_successful_order_id: Optional[str] = Field(
        None,
        description="ID of the last successfully completed order"
    )
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_1234567890",
                "whatsapp_number": "+923001234567",
                "preferences": {
                    "favorite_items": ["Pepperoni Classic", "Margherita"],
                    "diet_type": "non-veg",
                    "preferred_size": "large",
                    "payment_method": "cod"
                },
                "behavior_patterns": {
                    "frequent_order_time": "evening",
                    "average_order_value": 25.50,
                    "order_count": 5
                },
                "language_preference": "roman_urdu",
                "last_successful_order_id": "ORD-123456"
            }
        }


class SessionState(BaseModel):
    """
    Structured session state model
    Compressed representation of conversation for token efficiency
    """
    session_id: str = Field(..., description="Session/user identifier")
    recent_intents: List[str] = Field(
        default_factory=list,
        description="Recent detected intents"
    )
    entities: Dict[str, List[Any]] = Field(
        default_factory=dict,
        description="Extracted entities (items, quantities, preferences)"
    )
    last_action: str = Field(
        default="none",
        description="Last action taken in session"
    )
    language_hint: str = Field(
        default="english",
        description="Detected language in current session"
    )
    message_count: int = Field(
        default=0,
        description="Number of messages in session"
    )
    has_pending_order: bool = Field(
        default=False,
        description="Whether there's a pending order awaiting confirmation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "guest_session_123",
                "recent_intents": ["search_menu", "create_order", "confirmation"],
                "entities": {
                    "mentioned_pizzas": ["pepperoni"],
                    "quantities": [2],
                    "preferences": ["large", "spicy"]
                },
                "last_action": "confirming_order",
                "language_hint": "roman_urdu",
                "message_count": 5,
                "has_pending_order": True
            }
        }


def create_default_preferences(user_id: str, whatsapp_number: Optional[str] = None) -> Dict[str, Any]:
    """
    Create default user preferences dictionary
    
    Args:
        user_id: User identifier
        whatsapp_number: Optional WhatsApp number
        
    Returns:
        Dictionary with default preference structure
    """
    return {
        "user_id": user_id,
        "whatsapp_number": whatsapp_number,
        "preferences": {
            "favorite_items": [],
            "diet_type": "mixed",
            "preferred_size": "medium",
            "payment_method": "cod"
        },
        "behavior_patterns": {
            "frequent_order_time": "unknown",
            "average_order_value": 0.0,
            "order_count": 0
        },
        "language_preference": "english",
        "last_successful_order_id": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


def merge_preference_update(
    existing: Dict[str, Any],
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge preference updates intelligently
    
    Args:
        existing: Existing preferences
        updates: New updates to merge
        
    Returns:
        Merged preferences dictionary
    """
    merged = existing.copy()
    
    # Update top-level fields
    for key in ["language_preference", "last_successful_order_id"]:
        if key in updates and updates[key] is not None:
            merged[key] = updates[key]
    
    # Deep merge preferences
    if "preferences" in updates:
        if "preferences" not in merged:
            merged["preferences"] = {}
        merged["preferences"].update(updates["preferences"])
    
    # Deep merge behavior patterns
    if "behavior_patterns" in updates:
        if "behavior_patterns" not in merged:
            merged["behavior_patterns"] = {}
        merged["behavior_patterns"].update(updates["behavior_patterns"])
    
    # Update timestamp
    merged["updated_at"] = datetime.utcnow()
    
    return merged
