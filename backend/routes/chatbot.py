"""
Chatbot Route - Main agent interaction endpoint
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from agent import get_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request payload"""
    message: str
    user_id: str = "guest"
    conversation_id: Optional[str] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None


class ChatResponse(BaseModel):
    """Chat response payload"""
    reply: str
    tool_used: Optional[str] = None
    status: str = "success"
    timestamp: Optional[str] = None
    thought: Optional[str] = None


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chatbot endpoint - processes user messages through the agent
    
    The agent will:
    1. Detect language (English/Roman Urdu/Roman Hindi)
    2. Check for pending order confirmation
    3. Analyze the user's message
    4. Decide whether to use a tool or respond directly
    5. Execute tools if needed
    6. Return a formatted response
    """
    try:
        from datetime import datetime
        from utils.multilingual import detect_roman_urdu_hindi, get_multilingual_prompt_prefix
        from utils.memory import get_conversation_memory
        from utils.db import get_db
        
        # Get conversation memory and database
        memory = get_conversation_memory()
        db = get_db()
        
        # === PHASE 2 & 3: Load long-term memory ===
        user_prefs = db.get_user_preferences(request.user_id)
        
        # Log memory read
        if user_prefs:
            logger.debug(f"📚 Loaded user preferences for {request.user_id}")
        else:
            logger.debug(f"📚 No existing preferences for {request.user_id}")
        
        # Detect multilingual input and persist language
        is_multilingual = detect_roman_urdu_hindi(request.message)
        multilingual_prefix = get_multilingual_prompt_prefix(request.message)
        
        detected_language = "english"
        if is_multilingual:
            detected_language = "roman_urdu"
            logger.info(f"🌐 Detected Roman Urdu/Hindi from {request.user_id}")
            
            # Store language preference if changed
            current_lang = user_prefs.get("language_preference") if user_prefs else None
            if current_lang != detected_language:
                db.update_language_preference(request.user_id, detected_language)
                logger.info(f"💾 Updated language preference to {detected_language}")
        
        # Add conversation context if provided
        conversation_history = request.conversation_history or []
        
        # Add user message to memory
        memory.add_message(request.user_id, "user", request.message)
        
        # === PHASE 1: Compress history for token efficiency ===
        compressed_state = memory.compress_history(request.user_id)
        logger.debug(f"🗜️ Compressed state: {len(str(compressed_state))} chars")
        
        # Check for order confirmation (yes, haan, ok, theek hai, etc.)
        confirmation_keywords = ['yes', 'haan', 'ha', 'confirm', 'ok', 'okay', 'theek hai', 'acha', 'sure', 'book karo', 'karo']
        user_message_lower = request.message.lower()
        is_confirmation = any(keyword in user_message_lower for keyword in confirmation_keywords)
        
        # Check if there's a pending order
        pending_order = memory.get_pending_order(request.user_id)
        
        if pending_order and is_confirmation:
            # User is confirming a pending order - execute it now
            logger.info(f"✅ User {request.user_id} confirmed pending order")
            logger.debug(f"📦 Pending order details: {pending_order}")
            
            # Validate that pending order has items
            items = pending_order.get("items", [])
            if not items or len(items) == 0:
                logger.warning(f"⚠️ Pending order for {request.user_id} has no items")
                reply_text = "I'm sorry, I don't have any items in your pending order. Could you please tell me what pizza you'd like to order?"
                memory.add_message(request.user_id, "assistant", reply_text)
                memory.clear_pending_order(request.user_id)
                
                return ChatResponse(
                    reply=reply_text,
                    status="error",
                    timestamp=datetime.utcnow().isoformat()
                )
            
            # Execute the pending order
            from agent.tools_registry import get_tool_registry
            tool_registry = get_tool_registry()
            result = tool_registry.execute_tool("create_order", pending_order)
            
            # Clear pending order
            memory.clear_pending_order(request.user_id)
            
            if result.get("success"):
                order_result = result.get("result", {})
                if order_result.get("success"):
                    order_id = order_result.get("order_id", "N/A")
                    total = order_result.get("total", 0)
                    items = order_result.get("items", [])
                    
                    # === PHASE 3: Track order completion in long-term memory ===
                    try:
                        db.track_order_completion(
                            user_id=request.user_id,
                            order_id=order_id,
                            items=items,
                            total=total
                        )
                        logger.info(f"💾 Tracked order completion for {request.user_id}")
                    except Exception as e:
                        logger.error(f"❌ Failed to track order: {e}")
                    
                    reply_text = f"🎉 Order confirmed!\n\n📋 Order ID: {order_id}\n💰 Total: ${total}\n\n✅ Your pizza will be delivered in 25-35 minutes!"
                else:
                    error_msg = order_result.get('error', 'Unknown error')
                    logger.error(f"❌ Order creation failed: {error_msg}")
                    reply_text = f"❌ Sorry, there was an issue placing your order: {error_msg}. Please try ordering again."
            else:
                error_msg = result.get('error', 'Tool execution failed')
                logger.error(f"❌ Tool execution failed: {error_msg}")
                reply_text = "❌ Sorry, I couldn't complete your order. Please try again."
            
            memory.add_message(request.user_id, "assistant", reply_text)
            
            return ChatResponse(
                reply=reply_text,
                tool_used="create_order",
                status="success",
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Get agent
        agent = get_agent()
        
        # Process message with multilingual awareness
        if is_multilingual:
            logger.info(f"Detected Roman Urdu/Hindi input from {request.user_id}")
        
        result = agent.run(
            user_message=request.message,
            user_id=request.user_id,
            conversation_history=conversation_history,
            auto_execute_tools=True
        )
        
        # Format response based on result type
        response_type = result.get("type", "reply")
        
        if response_type == "reply":
            # Direct reply from agent
            return ChatResponse(
                reply=result.get("content", "I'm not sure how to respond to that."),
                tool_used=None,
                status="success",
                timestamp=result.get("timestamp")
            )
        
        elif response_type == "tool_result":
            # Tool was executed successfully
            tool_name = result.get("tool")
            tool_result = result.get("result")
            thought = result.get("thought", "")
            
            # Format reply based on tool
            reply = _format_tool_result(tool_name, tool_result, thought)
            
            return ChatResponse(
                reply=reply,
                tool_used=tool_name,
                status="success",
                timestamp=result.get("timestamp"),
                thought=thought
            )
        
        elif response_type == "error":
            # Tool execution failed
            error_msg = result.get("error", "Unknown error")
            return ChatResponse(
                reply=f"I encountered an error: {error_msg}. Please try again or rephrase your request.",
                tool_used=result.get("tool"),
                status="error",
                timestamp=result.get("timestamp")
            )
        
        else:
            # Unknown response type
            return ChatResponse(
                reply="I received your message but I'm not sure how to respond. Please try rephrasing.",
                status="error"
            )
    
    except Exception as e:
        logger.error(f"Error in chatbot endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def _format_tool_result(tool_name: str, tool_result: Any, thought: str = "") -> str:
    """Format tool results into user-friendly responses"""
    
    try:
        if tool_name == "search_kb":
            # Format knowledge base results
            if isinstance(tool_result, list) and len(tool_result) > 0:
                top_result = tool_result[0]
                text = top_result.get("text", "")
                category = top_result.get("metadata", {}).get("category", "")
                
                response = f"📚 **{category}**\n\n{text}"
                
                # Add additional results if available
                if len(tool_result) > 1:
                    response += "\n\n**Related Information:**"
                    for result in tool_result[1:]:
                        metadata = result.get("metadata", {})
                        title = metadata.get("title", "")
                        if title:
                            response += f"\n• {title}"
                
                return response
            else:
                return "I couldn't find specific information about that in our knowledge base. Is there anything else I can help you with?"
        
        elif tool_name == "search_menu":
            # Format menu search results
            if isinstance(tool_result, list) and len(tool_result) > 0:
                response = f"🍕 **Found {len(tool_result)} pizza(s):**\n\n"
                
                for idx, item in enumerate(tool_result[:5], 1):  # Limit to 5
                    name = item.get("name", "Unknown")
                    price = item.get("price", 0)
                    category = item.get("category", "")
                    description = item.get("description", "")[:100]
                    
                    response += f"{idx}. **{name}** - ${price:.2f} ({category})\n"
                    response += f"   {description}\n\n"
                
                if len(tool_result) > 5:
                    response += f"...and {len(tool_result) - 5} more! Would you like to see more options?"
                
                return response
            else:
                return "I couldn't find any pizzas matching that description. Would you like to see our full menu or try a different search?"
        
        elif tool_name == "create_order":
            # Format order creation result
            if isinstance(tool_result, dict) and tool_result.get("success"):
                order_id = tool_result.get("order_id", "")
                total = tool_result.get("total", 0)
                
                return f"✅ **Order Created Successfully!**\n\nOrder ID: `{order_id}`\nTotal: ${total:.2f}\n\nYour order has been placed and will be ready soon! You can track it using the order ID."
            else:
                error = tool_result.get("error", "Unknown error")
                return f"❌ Sorry, I couldn't create your order: {error}. Please try again or contact support."
        
        elif tool_name == "update_order":
            # Format order update result
            if isinstance(tool_result, dict) and tool_result.get("success"):
                order_id = tool_result.get("order_id", "")
                return f"✅ Order `{order_id}` has been updated successfully!"
            else:
                error = tool_result.get("error", "Unknown error")
                return f"❌ Couldn't update order: {error}"
        
        elif tool_name == "order_status":
            # Format order status result
            if isinstance(tool_result, dict) and tool_result.get("success"):
                order_id = tool_result.get("order_id", "")
                status = tool_result.get("status", "unknown")
                total = tool_result.get("total", 0)
                
                response = f"📦 **Order Status**\n\nOrder ID: `{order_id}`\nStatus: **{status.upper()}**\nTotal: ${total:.2f}\n"
                
                # Add tracking timeline
                tracking = tool_result.get("tracking", [])
                if tracking:
                    response += "\n**Timeline:**\n"
                    for event in tracking:
                        event_status = event.get("status", "")
                        response += f"• {event_status.capitalize()}\n"
                
                return response
            else:
                error = tool_result.get("error", "Order not found")
                return f"❌ {error}"
        
        elif tool_name == "recommend_pizza":
            # Format recommendations
            if isinstance(tool_result, list) and len(tool_result) > 0:
                response = "🎯 **Recommended Pizzas for You:**\n\n"
                
                for idx, item in enumerate(tool_result, 1):
                    name = item.get("name", "Unknown")
                    price = item.get("price", 0)
                    reason = item.get("recommendation_reason", "Great choice!")
                    
                    response += f"{idx}. **{name}** - ${price:.2f}\n"
                    response += f"   _{reason}_\n\n"
                
                response += "Would you like to order any of these?"
                return response
            else:
                return "I couldn't generate recommendations right now. Would you like to browse our menu instead?"
        
        elif tool_name == "ask_llm":
            # Format LLM response
            if isinstance(tool_result, dict) and tool_result.get("success"):
                return tool_result.get("response", "I'm not sure how to answer that.")
            else:
                return "I apologize, I'm having trouble answering that question right now."
        
        else:
            # Default format
            return str(tool_result)
    
    except Exception as e:
        logger.error(f"Error formatting tool result: {e}")
        return "I completed the action but had trouble formatting the response. The operation was successful."


@router.get("/health")
async def chatbot_health():
    """Health check for chatbot service"""
    return {"status": "healthy", "service": "chatbot"}


@router.get("/session/{user_id}")
async def get_session(user_id: str):
    """
    Retrieve chat session history
    
    Args:
        user_id: User identifier
        
    Returns:
        Session history with last 25 messages
    """
    try:
        from utils.memory import get_conversation_memory
        
        memory = get_conversation_memory()
        history = memory.get_history(user_id, last_n=25)
        
        # Convert datetime to ISO strings for JSON response
        serialized_history = []
        for msg in history:
            serialized_msg = msg.copy()
            if 'timestamp' in serialized_msg and hasattr(serialized_msg['timestamp'], 'isoformat'):
                serialized_msg['timestamp'] = serialized_msg['timestamp'].isoformat()
            serialized_history.append(serialized_msg)
        
        return {
            "user_id": user_id,
            "message_count": len(serialized_history),
            "messages": serialized_history
        }
    except Exception as e:
        logger.error(f"Error retrieving session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session/{user_id}")
async def clear_session(user_id: str):
    """
    Clear chat session for a user
    
    Args:
        user_id: User identifier
        
    Returns:
        Confirmation of deletion
    """
    try:
        from utils.memory import get_conversation_memory
        from utils.db import get_db
        
        memory = get_conversation_memory()
        db = get_db()
        
        # Clear from memory
        memory.clear_history(user_id)
        
        # Clear from database
        db.delete_chat_session(user_id)
        
        logger.info(f"Cleared session for user {user_id}")
        
        return {
            "success": True,
            "message": f"Session cleared for user {user_id}"
        }
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
