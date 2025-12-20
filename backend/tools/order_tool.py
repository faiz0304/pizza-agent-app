"""
Order Tool - Create, update, and retrieve orders
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import random
import string

from utils.db import get_db

logger = logging.getLogger(__name__)


def generate_order_id() -> str:
    """Generate unique order ID"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"ORD-{timestamp}-{random_suffix}"


def create_order(
    user: Dict[str, Any],
    items: List[Dict[str, Any]],
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a new order
    
    Args:
        user: User information dict (must contain user_id)
        items: List of cart items with menu_id, name, qty, variant, price
        metadata: Optional metadata (delivery_address, payment info, etc.)
        
    Returns:
        Created order dict with order_id
    """
    try:
        # Validate inputs
        if not user or "user_id" not in user:
            raise ValueError("User information with user_id is required")
        
        if not items or len(items) == 0:
            raise ValueError("At least one item is required to create an order")
        
        # Calculate total
        total = sum(item.get("price", 0) * item.get("qty", 1) for item in items)
        
        # Generate order ID
        order_id = generate_order_id()
        
        # Build order document
        order_data = {
            "order_id": order_id,
            "user_id": user["user_id"],
            "items": items,
            "total": round(total, 2),
            "status": "created",
            "timestamps": {
                "created": datetime.utcnow(),
                "updated": datetime.utcnow()
            },
            "tracking": [
                {
                    "status": "created",
                    "timestamp": datetime.utcnow(),
                    "message": "Order created successfully"
                }
            ]
        }
        
        # Add optional metadata
        if metadata:
            if "delivery_address" in metadata:
                order_data["delivery_address"] = metadata["delivery_address"]
            if "payment" in metadata:
                order_data["payment"] = metadata["payment"]
            else:
                order_data["payment"] = {"method": "cash_on_delivery", "status": "pending"}
        
        # Save to database
        db = get_db()
        db.create_order(order_data)
        
        logger.info(f"✅ Order created: {order_id} for user {user['user_id']}")
        
        return {
            "success": True,
            "order_id": order_id,
            "message": f"Order {order_id} created successfully!",
            "total": order_data["total"],
            "status": order_data["status"]
        }
        
    except Exception as e:
        logger.error(f"❌ Error creating order: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create order"
        }


def update_order(order_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing order
    
    Args:
        order_id: Order ID to update
        updates: Dict of fields to update
        
    Returns:
        Result dict with success status
    """
    try:
        db = get_db()
        
        # Get existing order
        existing_order = db.get_order(order_id)
        if not existing_order:
            return {
                "success": False,
                "error": "Order not found",
                "message": f"Order {order_id} does not exist"
            }
        
        # Add timestamp
        updates["timestamps.updated"] = datetime.utcnow()
        
        # If status is being updated, add to tracking
        if "status" in updates:
            new_status = updates["status"]
            tracking_entry = {
                "status": new_status,
                "timestamp": datetime.utcnow(),
                "message": f"Order status updated to {new_status}"
            }
            
            # Update both status and tracking
            db.update_order(order_id, {
                "status": new_status,
                "timestamps.updated": datetime.utcnow(),
                "$push": {"tracking": tracking_entry}
            })
            
        else:
            # Regular update
            db.update_order(order_id, updates)
        
        logger.info(f"✅ Order updated: {order_id}")
        
        # Get updated order
        updated_order = db.get_order(order_id)
        updated_order.pop('_id', None)
        
        return {
            "success": True,
            "order_id": order_id,
            "message": "Order updated successfully",
            "order": updated_order
        }
        
    except Exception as e:
        logger.error(f"❌ Error updating order: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update order"
        }


def order_status(order_id: str) -> Dict[str, Any]:
    """
    Get order status and tracking information
    
    Args:
        order_id: Order ID to check
        
    Returns:
        Order status and tracking info
    """
    try:
        db = get_db()
        order = db.get_order(order_id)
        
        if not order:
            return {
                "success": False,
                "error": "Order not found",
                "message": f"No order found with ID {order_id}"
            }
        
        # Remove MongoDB _id
        order.pop('_id', None)
        
        # Extract key information
        result = {
            "success": True,
            "order_id": order["order_id"],
            "status": order["status"],
            "total": order["total"],
            "created": order["timestamps"]["created"],
            "updated": order["timestamps"]["updated"],
            "tracking": order.get("tracking", []),
            "items_count": len(order.get("items", []))
        }
        
        # Add delivery address if exists
        if "delivery_address" in order:
            result["delivery_address"] = order["delivery_address"]
        
        logger.info(f"Retrieved status for order: {order_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error getting order status: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve order status"
        }


def get_user_order_history(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get order history for a user
    
    Args:
        user_id: User ID
        limit: Maximum number of orders to return
        
    Returns:
        List of orders
    """
    try:
        db = get_db()
        orders = db.get_user_orders(user_id, limit)
        
        # Format results
        formatted_orders = []
        for order in orders:
            order.pop('_id', None)
            formatted_orders.append(order)
        
        logger.info(f"Retrieved {len(formatted_orders)} orders for user {user_id}")
        return formatted_orders
        
    except Exception as e:
        logger.error(f"❌ Error getting user orders: {e}")
        return []
