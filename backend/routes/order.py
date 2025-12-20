"""
Order Routes - Order management endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from tools.order_tool import (
    create_order,
    update_order,
    order_status,
    get_user_order_history
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order", tags=["orders"])


class CartItem(BaseModel):
    """Cart item model"""
    menu_id: str
    name: str
    qty: int
    variant: str
    price: float


class DeliveryAddress(BaseModel):
    """Delivery address model"""
    street: str
    city: str
    zip: str
    phone: Optional[str] = None


class PaymentInfo(BaseModel):
    """Payment information"""
    method: str
    status: str = "pending"


class CreateOrderRequest(BaseModel):
    """Create order request"""
    user_id: str
    items: List[CartItem]
    delivery_address: Optional[DeliveryAddress] = None
    payment: Optional[PaymentInfo] = None


class UpdateOrderRequest(BaseModel):
    """Update order request"""
    status: Optional[str] = None
    delivery_address: Optional[Dict[str, Any]] = None
    payment: Optional[Dict[str, Any]] = None


@router.post("/")
async def create_order_endpoint(request: dict):
    """
    Create a new pizza order
    
    Request body:
    - user: User information (name, email, phone, address)
    - items: List of cart items (menu_id, name, qty, variant, price)
    - metadata: Optional metadata including payment info
    """
    try:
        # Extract data from request
        user_info = request.get("user", {})
        items = request.get("items", [])
        metadata = request.get("metadata", {})
        
        # Build user object for order tool
        user = {
            "user_id": user_info.get("email", "guest"),  # Use email as user_id
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "phone": user_info.get("phone")
        }
        
        # Add address to metadata if present
        if "address" in user_info:
            metadata["delivery_address"] = user_info["address"]
        
        # Create order
        result = create_order(user, items, metadata)
        
        if result.get("success"):
            logger.info(f"Order created: {result.get('order_id')}")
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to create order"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}")
async def get_order_status(order_id: str):
    """
    Get order status and details
    
    Path Parameters:
    - order_id: Order identifier
    """
    try:
        result = order_status(order_id)
        
        if result.get("success"):
            return result
        else:
            raise HTTPException(status_code=404, detail=result.get("error", "Order not found"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{order_id}")
async def update_order_endpoint(order_id: str, request: UpdateOrderRequest):
    """
    Update an existing order
    
    Path Parameters:
    - order_id: Order identifier
    
    Request body:
    - status: Optional new status
    - delivery_address: Optional updated delivery address
    - payment: Optional updated payment info
    """
    try:
        # Build updates dict
        updates = {}
        if request.status:
            updates["status"] = request.status
        if request.delivery_address:
            updates["delivery_address"] = request.delivery_address
        if request.payment:
            updates["payment"] = request.payment
        
        if not updates:
            raise HTTPException(status_code=400, detail="No updates provided")
        
        # Update order
        result = update_order(order_id, updates)
        
        if result.get("success"):
            logger.info(f"Order updated: {order_id}")
            return result
        else:
            raise HTTPException(status_code=404, detail=result.get("error", "Order not found"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/history")
async def get_order_history(user_id: str, limit: int = 10):
    """
    Get order history for a user
    
    Path Parameters:
    - user_id: User identifier
    
    Query Parameters:
    - limit: Maximum number of orders to return (default: 10)
    """
    try:
        orders = get_user_order_history(user_id, limit)
        
        logger.info(f"Retrieved {len(orders)} orders for user {user_id}")
        
        return {
            "user_id": user_id,
            "orders": orders,
            "count": len(orders)
        }
    
    except Exception as e:
        logger.error(f"Error getting order history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
