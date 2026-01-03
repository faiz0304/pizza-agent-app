"""
Agent Core - Autonomous agent with tool-using capabilities
"""
import json
import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime

from agent.tools_registry import get_tool_registry
from utils.hf_client import generate_text

logger = logging.getLogger(__name__)


class AgentX:
    """
    AGENT-X: Autonomous Pizza Ordering Assistant
    
    Capabilities:
    - Understands user intent and extracts entities
    - Plans and executes tool calls
    - Maintains conversation context
    - Provides helpful responses
    """
    
    def __init__(self):
        self.name = "AGENT-X"
        self.tool_registry = get_tool_registry()
        self.max_iterations = 5
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the agent's system prompt with available tools"""
        
        tools_list = self.tool_registry.list_tools()
        tools_description = "\n".join([
            f"- {name}: {desc}" for name, desc in tools_list.items()
        ])
        
        prompt = f"""You are {self.name}, an intelligent pizza ordering assistant with advanced reasoning and multilingual capabilities.

CORE CAPABILITIES:
- Order pizzas and manage orders
- Provide accurate recommendations  
- Answer questions (menu, delivery, payments, allergens, hours)
- Track order status
- Understand English, Roman Urdu, and Roman Hindi
- Provide excellent customer service

AVAILABLE TOOLS:
{tools_description}

INTENT DETECTION PATTERNS:

1. MENU QUERIES → search_menu:
   "What pizzas?", "vegetarian options", "spicy pizza", "mujhe pizza dikhao", "kya options hain"

2. INFO QUERIES → search_kb:
   "store hours", "delivery time", "refund policy", "kab band", "delivery kitne time"

3. ORDER CREATION FLOW (2-STEP PROCESS):
   
   STEP 1 - User wants to order → SUGGEST and ASK FOR CONFIRMATION (NO tool call yet!)
   Examples:
   - "meat lover pizza book krdo"
   - "I want pepperoni"
   - "bohat bhook lagi kuch bhi order krdo"
   
   Response format:
   {{"reply": "Great! I'll order [Pizza Name] ([Size], $[Price]). Should I confirm this order? (haan/yes to confirm)"}}
   
   STEP 2 - User confirms → NOW use create_order tool
   Confirmation keywords: "yes", "haan", "ha", "confirm", "book karo", "theek hai", "acha", "ok", "sure"
   
   Response format:
   {{"thought": "User confirmed, creating order", "tool": "create_order", "tool_input": {{...}}}}

4. TRACKING → order_status:
   "track order ORD-123", "where is my order", "mera order kahan"

5. GREETINGS → direct reply (NO tool):
   "Hi", "Hello", "Salaam", "Kya hal", "Thanks", "Shukriya"

MULTILINGUAL (Roman Urdu/Hindi):
Understand: salaam, kya hal, kya (what), kahan (where), kitna (how much), dikhao (show), batao (tell), chahiye (want), haan (yes), nahi (no), acha (okay), ek/do/teen (1/2/3), book krdo (book it), order karo (order it), bhook lagi (hungry), apni marzi (your choice), theek hai (okay/fine)
→ Respond in English but be friendly and acknowledge their language

ORDER CONFIRMATION EXAMPLES:

User: "meat lover pizza book krdo"
{{"reply": "Perfect! I'll order 1 Meat Lovers Pizza (Medium, $14.99). Should I confirm this order? Reply 'haan' or 'yes' to proceed! 🍕"}}

User: "haan book karo"
{{"thought": "User confirmed the order", "tool": "create_order", "tool_input": {{"user": {{"user_id": "guest"}}, "items": [{{"name": "Meat Lovers", "qty": 1, "variant": "medium", "price": 14.99}}]}}}}

User: "bohat bhook lagi kuch order krdo"
{{"reply": "I understand you're very hungry! I recommend our popular Pepperoni Classic (Medium, $12.99). Shall I place this order? Just say 'yes' or 'haan'! 😊"}}

User: "yes please"
{{"thought": "User confirmed, placing Pepperoni order", "tool": "create_order", "tool_input": {{"user": {{"user_id": "guest"}}, "items": [{{"name": "Pepperoni Classic", "qty": 1, "variant": "medium", "price": 12.99}}]}}}}

User: "2 large pepperoni"
{{"reply": "Got it! 2 Large Pepperoni Classic pizzas for $27.98. Should I confirm your order? (yes/haan)"}}

User: "theek hai"
{{"thought": "User said theek hai (okay), confirming order", "tool": "create_order", "tool_input": {{"user": {{"user_id": "guest"}}, "items": [{{"name": "Pepperoni Classic", "qty": 2, "variant": "large", "price": 13.99}}]}}}}

RESPONSE FORMAT (MUST BE VALID JSON):

Tool call:
{{"thought": "reasoning", "tool": "tool_name", "tool_input": {{"param": "value"}}}}

Direct reply:
{{"reply": "your message"}}

OTHER EXAMPLES:

User: "mujhe spicy pizza dikhao"
{{"thought": "Roman Urdu: wants to see spicy pizzas", "tool": "search_menu", "tool_input": {{"query": "spicy"}}}}

User: "delivery kitne time mein?"
{{"thought": "Roman Urdu: asking delivery time", "tool": "search_kb", "tool_input": {{"query": "delivery time"}}}}

User: "Salaam, kaisay ho?"
{{"reply": "Salaam! I'm great, thank you! 👋 How can I help you order pizza today?"}}

GUIDELINES:
✅ NEVER create orders without confirmation - ALWAYS ask first!
✅ When user wants to order, SUGGEST the pizza and ASK for confirmation
✅ Only call create_order tool AFTER user confirms with: yes, haan, ha, confirm, ok, theek hai, acha
✅ Remember pending order details in conversation context
✅ For vague orders, recommend popular pizza (Pepperoni/Margherita)
✅ Default to medium size and cash on delivery
✅ Understand context from previous messages (last 5 messages matter!)
✅ Be helpful with any language
✅ Keep responses clear and concise
✅ Use emojis appropriately 🍕

Respond with VALID JSON ONLY:"""

        return prompt
    
    def process_message(
        self, 
        user_message: str, 
        user_id: str = "guest",
        conversation_history: Optional[List[Dict]] = None,
        memory_context: str = ""
    ) -> Dict[str, Any]:
        """
        Process a user message and return agent's decision or response
        
        Args:
            user_message: User's input message
            user_id: User identifier
            conversation_history: Optional list of previous messages
            memory_context: Optional memory-aware context string
            
        Returns:
            Dict with agent's response or tool call
        """
        try:
            logger.info(f"Processing message from user {user_id}: {user_message[:100]}")
            
            # Build context
            context = self._build_context(user_message, conversation_history)
            
            # Build prompt with memory context
            prompt_parts = [self.system_prompt]
            
            if memory_context:
                prompt_parts.append(f"\n--- Memory Context ---\n{memory_context}\n")
            
            prompt_parts.append(f"\nUser Message: {user_message}\n\nYour JSON Response:")
            full_prompt = "".join(prompt_parts)
            
            llm_response = generate_text(full_prompt, max_tokens=800, temperature=0.7)
            
            # Parse JSON response
            agent_decision = self._parse_agent_response(llm_response)
            
            # Add metadata
            agent_decision["timestamp"] = datetime.utcnow().isoformat()
            agent_decision["user_id"] = user_id
            
            logger.info(f"Agent decision: {agent_decision.get('thought', agent_decision.get('reply', ''))[:100]}")
            
            return agent_decision
            
        except Exception as e:
            logger.error(f"Error in agent processing: {e}")
            return {
                "reply": "I apologize, but I encountered an error processing your request. Please try again or rephrase your message.",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _parse_agent_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse LLM response and extract JSON with robust error handling"""
        try:
            # Remove markdown code blocks if present
            cleaned_response = re.sub(r'```json\s*', '', llm_response)
            cleaned_response = re.sub(r'```\s*', '', cleaned_response)
            cleaned_response = cleaned_response.strip()
            
            # Try to parse entire response as JSON first
            try:
                parsed = json.loads(cleaned_response)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            
            # Try to find JSON object in response
            json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                try:
                    parsed = json.loads(json_str)
                    if isinstance(parsed, dict):
                        return parsed
                except json.JSONDecodeError:
                    pass
            
            # Fallback: treat entire response as direct reply
            logger.warning(f"Could not parse JSON from LLM response, treating as direct reply")
            logger.debug(f"Original LLM response: {llm_response[:200]}")
            return {"reply": llm_response}
                
        except Exception as e:
            logger.error(f"Unexpected error parsing LLM response: {e}")
            logger.debug(f"LLM response was: {llm_response[:200]}")
            # Ultimate fallback
            return {"reply": "I apologize, I'm having trouble formulating a response. Please try again."}
    
    def _build_context(
        self, 
        current_message: str, 
        history: Optional[List[Dict]] = None
    ) -> str:
        """Build conversation context for the agent"""
        if not history or len(history) == 0:
            return ""
        
        # Include last 3 messages for context
        recent_history = history[-3:] if len(history) > 3 else history
        context_parts = []
        
        for msg in recent_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def _build_memory_context(
        self,
        user_id: str,
        session_state: Optional[Dict[str, Any]] = None,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build memory-aware context from short-term and long-term memory
        
        Args:
            user_id: User identifier
            session_state: Compressed session state
            user_preferences: Long-term preferences
            
        Returns:
            Formatted context string for prompt
        """
        context_parts = []
        
        # Add long-term preferences
        if user_preferences:
            prefs = user_preferences.get("preferences", {})
            favorites = prefs.get("favorite_items", [])
            if favorites:
                fav_str = ", ".join(favorites[:3])  # Top 3
                context_parts.append(f"💾 User favorites: {fav_str}")
            
            lang_pref = user_preferences.get("language_preference")
            if lang_pref and lang_pref != "english":
                context_parts.append(f"🌐 Preferred language: {lang_pref}")
            
            order_count = user_preferences.get("behavior_patterns", {}).get("order_count", 0)
            if order_count > 0:
                context_parts.append(f"📊 Previous orders: {order_count}")
        
        # Add session state
        if session_state:
            intents = session_state.get("recent_intents", [])
            if intents:
                context_parts.append(f"🎯 Recent intents: {', '.join(intents[-2:])}")
            
            entities = session_state.get("entities", {})
            mentioned_pizzas = entities.get("mentioned_pizzas", [])
            if mentioned_pizzas:
                context_parts.append(f"🍕 Mentioned: {', '.join(mentioned_pizzas)}")
            
            has_pending = session_state.get("has_pending_order", False)
            if has_pending:
                context_parts.append("⚠️ PENDING ORDER awaiting confirmation")
        
        if not context_parts:
            return ""
        
        return "\n".join(context_parts)
    
    def execute_tool_call(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call and return results
        
        Args:
            tool_name: Name of tool to execute
            tool_input: Tool input parameters
            
        Returns:
            Tool execution result
        """
        return self.tool_registry.execute_tool(tool_name, tool_input)
    
    def run(
        self, 
        user_message: str, 
        user_id: str = "guest",
        conversation_history: Optional[List[Dict]] = None,
        auto_execute_tools: bool = True,
        user_preferences: Optional[Dict[str, Any]] = None,
        session_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the agent: process message and optionally execute tools
        
        Args:
            user_message: User's input message
            user_id: User identifier
            conversation_history: Optional conversation history
            auto_execute_tools: If True, automatically execute tool calls
            user_preferences: Optional long-term user preferences
            session_state: Optional compressed session state
            
        Returns:
            Final response with agent's reply or tool results
        """
        # Build memory-aware context
        memory_context = self._build_memory_context(
            user_id=user_id,
            session_state=session_state,
            user_preferences=user_preferences
        )
        
        # Log memory usage
        if memory_context:
            logger.debug(f"💾 Memory context: {len(memory_context)} chars")
        
        # Get agent's decision with memory context
        decision = self.process_message(
            user_message=user_message,
            user_id=user_id,
            conversation_history=conversation_history,
            memory_context=memory_context
        )
        
        # If it's a direct reply, return it
        if "reply" in decision:
            return {
                "type": "reply",
                "content": decision["reply"],
                "timestamp": decision.get("timestamp")
            }
        
        # If it's a tool call
        if "tool" in decision and auto_execute_tools:
            tool_name = decision["tool"]
            tool_input = decision.get("tool_input", {})
            thought = decision.get("thought", "")
            
            # Execute the tool
            tool_result = self.execute_tool_call(tool_name, tool_input)
            
            # Format response based on tool result
            if tool_result.get("success"):
                return {
                    "type": "tool_result",
                    "tool": tool_name,
                    "thought": thought,
                    "result": tool_result.get("result"),
                    "timestamp": decision.get("timestamp")
                }
            else:
                return {
                    "type": "error",
                    "tool": tool_name,
                    "thought": thought,
                    "error": tool_result.get("error"),
                    "timestamp": decision.get("timestamp")
                }
        
        # Return raw decision if not auto-executing
        return decision


# Global agent instance
agent_x = AgentX()


def get_agent() -> AgentX:
    """Get the global agent instance"""
    return agent_x
