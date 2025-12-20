"""
Database connection and utilities for MongoDB Atlas
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    """MongoDB Database Handler"""
    
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB_NAME", "pizza_db")
        self.client: Optional[MongoClient] = None
        self.db = None
        
    def connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            logger.info(f"✅ Connected to MongoDB: {self.db_name}")
            return True
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        if self.db is None:
            raise Exception("Database not connected. Call connect() first.")
        return self.db[collection_name]
    
    # Menu Collection Methods
    def get_menu_items(self, query: Optional[Dict] = None, limit: int = 50) -> List[Dict]:
        """Get menu items with optional query filter"""
        collection = self.get_collection("menu")
        query = query or {}
        return list(collection.find(query).limit(limit))
    
    def get_menu_item_by_id(self, item_id: str) -> Optional[Dict]:
        """Get single menu item by ID"""
        collection = self.get_collection("menu")
        return collection.find_one({"id": item_id})
    
    def search_menu(self, search_query: str) -> List[Dict]:
        """Full-text search in menu collection"""
        collection = self.get_collection("menu")
        # Search in name, description, ingredients, tags, category
        regex_pattern = {"$regex": search_query, "$options": "i"}
        query = {
            "$or": [
                {"name": regex_pattern},
                {"description": regex_pattern},
                {"ingredients": regex_pattern},
                {"tags": regex_pattern},
                {"category": regex_pattern}
            ]
        }
        return list(collection.find(query).limit(20))
    
    def insert_menu_item(self, item: Dict) -> str:
        """Insert new menu item"""
        collection = self.get_collection("menu")
        result = collection.insert_one(item)
        return str(result.inserted_id)
    
    # Order Collection Methods
    def create_order(self, order_data: Dict) -> str:
        """Create new order"""
        collection = self.get_collection("orders")
        result = collection.insert_one(order_data)
        return str(result.inserted_id)
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        collection = self.get_collection("orders")
        return collection.find_one({"order_id": order_id})
    
    def update_order(self, order_id: str, updates: Dict) -> bool:
        """Update order"""
        collection = self.get_collection("orders")
        result = collection.update_one(
            {"order_id": order_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def get_user_orders(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get orders for a specific user"""
        collection = self.get_collection("orders")
        return list(
            collection.find({"user_id": user_id})
            .sort("timestamps.created", -1)
            .limit(limit)
        )
    
    # Knowledge Base Collection Methods
    def get_kb_chunks(self, query: Optional[Dict] = None) -> List[Dict]:
        """Get knowledge base chunks"""
        collection = self.get_collection("customer_support_kb")
        query = query or {}
        return list(collection.find(query))
    
    def insert_kb_chunk(self, chunk: Dict) -> str:
        """Insert knowledge base chunk"""
        collection = self.get_collection("customer_support_kb")
        result = collection.insert_one(chunk)
        return str(result.inserted_id)
    
    def search_kb_text(self, search_query: str) -> List[Dict]:
        """Basic text search in KB (before vector search)"""
        collection = self.get_collection("customer_support_kb")
        regex_pattern = {"$regex": search_query, "$options": "i"}
        query = {
            "$or": [
                {"title": regex_pattern},
                {"text_chunk": regex_pattern},
                {"category": regex_pattern}
            ]
        }
        return list(collection.find(query).limit(10))
    
    # WhatsApp User Mapping Methods
    def get_or_create_user(self, whatsapp_number: str) -> Dict:
        """Get or create user mapping for WhatsApp number"""
        collection = self.get_collection("users")
        user = collection.find_one({"whatsapp_number": whatsapp_number})
        
        if not user:
            # Create new user
            from datetime import datetime
            user_data = {
                "user_id": f"user_{whatsapp_number.replace('+', '').replace(':', '_')}",
                "whatsapp_number": whatsapp_number,
                "created_at": datetime.utcnow(),
                "metadata": {}
            }
            collection.insert_one(user_data)
            return user_data
        
        return user


# Global database instance
db = Database()


def get_db() -> Database:
    """Get database instance (for dependency injection)"""
    if db.db is None:
        db.connect()
    return db
