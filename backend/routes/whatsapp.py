"""
WhatsApp Routes - Twilio WhatsApp webhook integration
"""
from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import Response
from typing import Optional
import logging
from twilio.rest import Client
from twilio.request_validator import RequestValidator
import os
from dotenv import load_dotenv

from agent import get_agent
from utils.db import get_db

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.info("✅ Twilio client initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Twilio client: {e}")


def send_whatsapp_message(to_number: str, message: str) -> bool:
    """
    Send a WhatsApp message via Twilio
    
    Args:
        to_number: Recipient WhatsApp number (format: whatsapp:+1234567890)
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    if not twilio_client:
        logger.error("Twilio client not initialized")
        return False
    
    try:
        # Ensure number has whatsapp: prefix
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"
        
        # Send message
        message_obj = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=to_number
        )
        
        logger.info(f"✅ WhatsApp message sent: {message_obj.sid}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send WhatsApp message: {e}")
        return False


@router.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...),
    To: Optional[str] = Form(None),
    ProfileName: Optional[str] = Form(None)
):
    """
    Twilio WhatsApp webhook endpoint
    
    This endpoint receives incoming WhatsApp messages from Twilio,
    processes them through the agent, and sends back responses.
    
    Form Parameters (from Twilio):
    - From: Sender's WhatsApp number (format: whatsapp:+1234567890)
    - Body: Message text
    - MessageSid: Unique message identifier
    - To: Recipient's number (your Twilio WhatsApp number)
    - ProfileName: Sender's WhatsApp profile name
    """
    try:
        logger.info(f"📱 WhatsApp message received from {From}: {Body[:100]}")
        
        # Extract phone number (remove 'whatsapp:' prefix)
        whatsapp_number = From.replace("whatsapp:", "")
        
        # Get or create user mapping
        db = get_db()
        user_data = db.get_or_create_user(From)
        user_id = user_data.get("user_id", "unknown")
        
        logger.info(f"Mapped WhatsApp number to user_id: {user_id}")
        
        # Process message through agent
        agent = get_agent()
        result = agent.run(
            user_message=Body,
            user_id=user_id,
            conversation_history=None,  # TODO: Implement conversation history storage
            auto_execute_tools=True
        )
        
        # Extract response text
        response_type = result.get("type", "reply")
        
        if response_type == "reply":
            response_text = result.get("content", "I'm sorry, I couldn't process your message.")
        
        elif response_type == "tool_result":
            # Format tool result (reuse chatbot formatting)
            from routes.chatbot import _format_tool_result
            tool_name = result.get("tool")
            tool_result = result.get("result")
            thought = result.get("thought", "")
            response_text = _format_tool_result(tool_name, tool_result, thought)
        
        elif response_type == "error":
            error_msg = result.get("error", "Unknown error")
            response_text = f"I encountered an error: {error_msg}. Please try again."
        
        else:
            response_text = "I received your message but I'm not sure how to respond."
        
        # Clean response for WhatsApp (remove markdown formatting that doesn't render well)
        response_text = _clean_response_for_whatsapp(response_text)
        
        # Send response via WhatsApp
        send_success = send_whatsapp_message(From, response_text)
        
        # Always return 200 OK to Twilio immediately
        if send_success:
            logger.info(f"✅ Response sent to {From}")
        else:
            logger.error(f"❌ Failed to send response to {From}")
        
        # Return empty 200 response (Twilio requirement)
        return Response(status_code=200)
    
    except Exception as e:
        logger.error(f"❌ Error processing WhatsApp webhook: {e}", exc_info=True)
        
        # Try to send error message to user
        try:
            error_response = "⚠️ I'm experiencing technical difficulties. Please try again in a moment."
            send_whatsapp_message(From, error_response)
        except:
            pass
        
        # Still return 200 OK to prevent Twilio retries
        return Response(status_code=200)


def _clean_response_for_whatsapp(text: str) -> str:
    """
    Clean response text for WhatsApp
    Removes or simplifies markdown that doesn't render well
    """
    import re
    
    # Remove markdown bold (**text** -> text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    
    # Remove code blocks (`text` -> text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # Keep emojis and basic formatting
    return text


@router.get("/status")
@router.post("/status")
async def whatsapp_status(
    MessageSid: Optional[str] = Form(None),
    MessageStatus: Optional[str] = Form(None),
    ErrorCode: Optional[str] = Form(None)
):
    """
    Check WhatsApp integration status or receive status callbacks from Twilio
    
    Handles both:
    - GET: Status check for integration health
    - POST: Twilio message delivery status callbacks
    """
    # If this is a status callback from Twilio (POST with form data)
    if MessageSid:
        logger.info(f"📊 Message status callback: {MessageSid} - {MessageStatus}")
        if ErrorCode:
            logger.error(f"❌ Message error: {ErrorCode}")
        return Response(status_code=200)
    
    # Otherwise, return integration status (GET request)
    configured = bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_WHATSAPP_NUMBER)
    client_ready = twilio_client is not None
    
    return {
        "configured": configured,
        "client_ready": client_ready,
        "status": "ready" if (configured and client_ready) else "not_configured"
    }


@router.post("/send")
async def send_message_endpoint(to: str, message: str):
    """
    Manual endpoint to send WhatsApp messages (for testing)
    
    Request body:
    - to: Recipient WhatsApp number
    - message: Message text
    """
    if not twilio_client:
        raise HTTPException(status_code=503, detail="Twilio client not initialized")
    
    success = send_whatsapp_message(to, message)
    
    if success:
        return {"status": "sent", "to": to}
    else:
        raise HTTPException(status_code=500, detail="Failed to send message")
