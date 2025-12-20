"""
Tools Registry - Centralized tool registration and execution
"""
import logging
from typing import Dict, Any, Callable, Optional

from tools.rag_tool import search_kb
from tools.menu_tool import search_menu
from tools.order_tool import create_order, update_order, order_status
from tools.recommend_tool import recommend_pizza
from utils.hf_client import generate_text

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Central registry for all agent tools
    Handles tool registration, validation, and execution
    """
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_descriptions: Dict[str, str] = {}
        self._register_all_tools()
    
    def _register_all_tools(self):
        """Register all available tools"""
        
        # RAG Tool
        self.register_tool(
            name="search_kb",
            function=search_kb,
            description="Search the knowledge base for customer support information about delivery, refunds, allergens, payments, etc. Returns top 3 relevant chunks."
        )
        
        # Menu Tool
        self.register_tool(
            name="search_menu",
            function=search_menu,
            description="Search menu items by name, description, ingredients, category, or tags. Returns matching pizza items."
        )
        
        # Order Tools
        self.register_tool(
            name="create_order",
            function=self._create_order_wrapper,
            description="Create a new pizza order. Requires user info, items list with menu_id/qty/variant, and optional delivery address."
        )
        
        self.register_tool(
            name="update_order",
            function=self._update_order_wrapper,
            description="Update an existing order by order_id. Can modify status, items, delivery address, etc."
        )
        
        self.register_tool(
            name="order_status",
            function=order_status,
            description="Get current order status and tracking information by order_id."
        )
        
        # Recommendation Tool
        self.register_tool(
            name="recommend_pizza",
            function=recommend_pizza,
            description="Get AI-powered pizza recommendations based on user preferences (spicy, cheesy, veg, non-veg, etc.)."
        )
        
        # LLM Tool
        self.register_tool(
            name="ask_llm",
            function=self._ask_llm_wrapper,
            description="Ask the LLM a general question or have a conversation when no specific tool is needed."
        )
        
        logger.info(f"✅ Registered {len(self.tools)} tools")
    
    def register_tool(self, name: str, function: Callable, description: str):
        """Register a new tool"""
        self.tools[name] = function
        self.tool_descriptions[name] = description
        logger.debug(f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a tool function by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools with descriptions"""
        return self.tool_descriptions.copy()
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given inputs
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Dictionary of input parameters
            
        Returns:
            Tool execution result
        """
        try:
            # Validate tool exists
            if tool_name not in self.tools:
                logger.error(f"Tool not found: {tool_name}")
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "available_tools": list(self.tools.keys())
                }
            
            # Get tool function
            tool_func = self.tools[tool_name]
            
            # Execute tool
            logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
            result = tool_func(**tool_input)
            
            logger.info(f"✅ Tool {tool_name} executed successfully")
            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }
            
        except TypeError as e:
            # Invalid parameters
            logger.error(f"Invalid parameters for tool {tool_name}: {e}")
            return {
                "success": False,
                "error": f"Invalid parameters: {str(e)}",
                "tool": tool_name
            }
            
        except Exception as e:
            # General execution error
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    # Wrapper functions for complex tool signatures
    
    def _create_order_wrapper(self, user: Optional[Dict] = None, items: Optional[list] = None, 
                              metadata: Optional[Dict] = None, user_info: Optional[Dict] = None,
                              user_data: Optional[Dict] = None, **kwargs):
        """
        Flexible wrapper for create_order to handle various parameter names
        Accepts: user, user_info, user_data (all map to same thing)
        """
        # Handle different parameter names for user info
        user_param = user or user_info or user_data or kwargs.get('user_id')
        
        # If user_param is just a string (user_id), convert to dict
        if isinstance(user_param, str):
            user_param = {"user_id": user_param}
        elif not user_param:
            # Default guest user
            user_param = {"user_id": "guest"}
        
        # Handle items
        items_param = items or kwargs.get('items', [])
        
        # Handle metadata
        metadata_param = metadata or kwargs.get('metadata', {})
        
        logger.info(f"Order wrapper called with user={user_param}, items={len(items_param)} items")
        
        return create_order(user_param, items_param, metadata_param)
    
    def _update_order_wrapper(self, order_id: str, updates: Optional[Dict] = None, metadata: Optional[Dict] = None, **kwargs):
        """Wrapper for update_order to handle metadata parameter gracefully"""
        # Merge all parameters into updates dict
        final_updates = updates or {}
        
        # If metadata is provided, merge it into updates
        if metadata:
            final_updates["metadata"] = metadata
        
        # Merge any additional kwargs
        final_updates.update(kwargs)
        
        return update_order(order_id, final_updates)
    
    def _ask_llm_wrapper(self, text: str, context: Optional[Dict] = None):
        """Wrapper for asking LLM general questions"""
        try:
            # Build context-aware prompt
            if context:
                context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                prompt = f"Context:\n{context_str}\n\nUser Question: {text}\n\nAnswer:"
            else:
                prompt = f"User Question: {text}\n\nAnswer:"
            
            # Generate response
            response = generate_text(prompt, max_tokens=500, temperature=0.7)
            
            return {
                "success": True,
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error in ask_llm: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global registry instance
tool_registry = ToolRegistry()


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance"""
    return tool_registry
