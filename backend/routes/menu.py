"""
Menu Routes - Menu browsing and search endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from tools.menu_tool import (
    search_menu,
    get_menu_item_by_id,
    get_all_menu_items,
    filter_menu_by_category
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/menu", tags=["menu"])


class MenuItem(BaseModel):
    """Menu item model"""
    id: str
    name: str
    price: float
    description: str
    ingredients: List[str]
    variants: Dict[str, float]
    category: str
    tags: List[str]
    images: List[str]


class MenuListResponse(BaseModel):
    """Menu list response"""
    items: List[Dict[str, Any]]
    count: int


@router.get("/", response_model=MenuListResponse)
async def get_menu(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=100, description="Max items to return")
):
    """
    Get all menu items with optional filtering
    
    Query Parameters:
    - category: Filter by category (veg, non-veg, etc.)
    - limit: Maximum number of items to return (1-100)
    """
    try:
        if category:
            items = filter_menu_by_category(category)
        else:
            items = get_all_menu_items(limit=limit)
        
        logger.info(f"Retrieved {len(items)} menu items")
        
        return MenuListResponse(
            items=items,
            count=len(items)
        )
    
    except Exception as e:
        logger.error(f"Error getting menu: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=MenuListResponse)
async def search_menu_endpoint(
    q: str = Query(..., min_length=1, description="Search query")
):
    """
    Search menu items by name, description, ingredients, or tags
    
    Query Parameters:
    - q: Search query string
    """
    try:
        results = search_menu(q)
        
        logger.info(f"Search '{q}' returned {len(results)} results")
        
        return MenuListResponse(
            items=results,
            count=len(results)
        )
    
    except Exception as e:
        logger.error(f"Error searching menu: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}")
async def get_menu_item(item_id: str):
    """
    Get a specific menu item by ID
    
    Path Parameters:
    - item_id: Menu item identifier
    """
    try:
        item = get_menu_item_by_id(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail=f"Menu item '{item_id}' not found")
        
        logger.info(f"Retrieved menu item: {item_id}")
        return item
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting menu item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/category/{category}")
async def get_menu_by_category(category: str):
    """
    Get menu items filtered by category
    
    Path Parameters:
    - category: Category name (veg, non-veg, spicy, etc.)
    """
    try:
        items = filter_menu_by_category(category)
        
        logger.info(f"Retrieved {len(items)} items in category '{category}'")
        
        return MenuListResponse(
            items=items,
            count=len(items)
        )
    
    except Exception as e:
        logger.error(f"Error filtering menu by category: {e}")
        raise HTTPException(status_code=500, detail=str(e))
