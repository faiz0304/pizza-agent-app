"""
Menu Tool - Search and retrieve menu items from MongoDB
"""
import logging
from typing import List, Dict, Any, Optional

from utils.db import get_db

logger = logging.getLogger(__name__)


def search_menu(query: str) -> List[Dict[str, Any]]:
    """
    Search menu items by name, description, ingredients, category, or tags
    
    Args:
        query: Search query string
        
    Returns:
        List of matching menu items
    """
    try:
        db = get_db()
        
        # Handle empty query - return all items (limited)
        if not query or not query.strip():
            logger.info("Empty query, returning all menu items")
            return db.get_menu_items(limit=20)
        
        # Search in database
        results = db.search_menu(query.strip())
        
        logger.info(f"Found {len(results)} menu items for query: '{query}'")
        
        # Format results (remove MongoDB _id field)
        formatted_results = []
        for item in results:
            item.pop('_id', None)  # Remove MongoDB internal ID
            formatted_results.append(item)
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error searching menu: {e}")
        return []


def get_menu_item_by_id(item_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific menu item by ID
    
    Args:
        item_id: Menu item ID
        
    Returns:
        Menu item dict or None if not found
    """
    try:
        db = get_db()
        item = db.get_menu_item_by_id(item_id)
        
        if item:
            item.pop('_id', None)
            logger.info(f"Retrieved menu item: {item_id}")
        else:
            logger.warning(f"Menu item not found: {item_id}")
        
        return item
        
    except Exception as e:
        logger.error(f"Error getting menu item: {e}")
        return None


def get_all_menu_items(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get all menu items
    
    Args:
        limit: Maximum number of items to return
        
    Returns:
        List of menu items
    """
    try:
        db = get_db()
        items = db.get_menu_items(limit=limit)
        
        # Format results
        formatted_results = []
        for item in items:
            item.pop('_id', None)
            formatted_results.append(item)
        
        logger.info(f"Retrieved {len(formatted_results)} menu items")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error getting menu items: {e}")
        return []


def filter_menu_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Filter menu items by category
    
    Args:
        category: Category name (veg, non-veg, spicy, etc.)
        
    Returns:
        List of matching menu items
    """
    try:
        db = get_db()
        query = {"category": {"$regex": category, "$options": "i"}}
        items = db.get_menu_items(query=query)
        
        # Format results
        formatted_results = []
        for item in items:
            item.pop('_id', None)
            formatted_results.append(item)
        
        logger.info(f"Found {len(formatted_results)} items in category: {category}")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error filtering menu by category: {e}")
        return []


def filter_menu_by_tags(tags: List[str]) -> List[Dict[str, Any]]:
    """
    Filter menu items by tags
    
    Args:
        tags: List of tag names
        
    Returns:
        List of matching menu items
    """
    try:
        db = get_db()
        query = {"tags": {"$in": tags}}
        items = db.get_menu_items(query=query)
        
        # Format results
        formatted_results = []
        for item in items:
            item.pop('_id', None)
            formatted_results.append(item)
        
        logger.info(f"Found {len(formatted_results)} items with tags: {tags}")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error filtering menu by tags: {e}")
        return []
