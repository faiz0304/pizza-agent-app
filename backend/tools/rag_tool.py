"""
RAG Tool - Knowledge Base Search using Chroma Vector Store
"""
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from utils.embeddings import embed_text

load_dotenv()

logger = logging.getLogger(__name__)


class RAGSearchTool:
    """
    Knowledge Base Search Tool using Chroma DB
    Performs semantic search over customer support knowledge base
    """
    
    def __init__(self):
        self.persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        self.collection_name = os.getenv("CHROMA_COLLECTION_NAME", "customer_support_kb")
        self.client = None
        self.collection = None
        self._initialize_chroma()
    
    def _initialize_chroma(self):
        """Initialize Chroma DB client and collection"""
        try:
            # Create Chroma client with persistent storage
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            
            # Get or create collection
            # Using default embedding function (can be customized)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Customer support knowledge base for pizza ordering"}
            )
            
            logger.info(f"✅ Chroma DB initialized: {self.collection_name}")
            logger.info(f"Collection count: {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Chroma DB: {e}")
            raise
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: List[Dict[str, Any]], 
        ids: List[str]
    ):
        """
        Add documents to the knowledge base
        
        Args:
            documents: List of text chunks
            metadatas: List of metadata dicts for each document
            ids: List of unique IDs for each document
        """
        try:
            # Generate embeddings
            embeddings = [embed_text(doc) for doc in documents]
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
            logger.info(f"Added {len(documents)} documents to knowledge base")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def search_kb(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search knowledge base using semantic similarity
        
        Args:
            query: Search query text
            top_k: Number of top results to return
            
        Returns:
            List of dicts with keys: text, metadata, score
        """
        try:
            # Handle empty query
            if not query or not query.strip():
                logger.warning("Empty search query provided")
                return []
            
            # Generate query embedding
            query_embedding = embed_text(query)
            
            # Search in Chroma
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            formatted_results = []
            if results and results.get("documents"):
                for idx in range(len(results["documents"][0])):
                    formatted_results.append({
                        "text": results["documents"][0][idx],
                        "metadata": results["metadatas"][0][idx] if results.get("metadatas") else {},
                        "score": results["distances"][0][idx] if results.get("distances") else 0.0,
                        "id": results["ids"][0][idx] if results.get("ids") else None
                    })
            
            logger.info(f"Found {len(formatted_results)} results for query: '{query[:50]}...'")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_dir": self.persist_dir
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}


# Global RAG tool instance
rag_tool = RAGSearchTool()


def search_kb(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Convenience function for knowledge base search
    
    Args:
        query: Search query
        top_k: Number of results to return
        
    Returns:
        List of relevant KB chunks with metadata and scores
    """
    return rag_tool.search_kb(query, top_k)


def initialize_knowledge_base():
    """
    Initialize knowledge base with sample customer support content
    Should be called once during app startup
    """
    # Check if KB already has content
    if rag_tool.collection.count() > 0:
        logger.info("Knowledge base already initialized")
        return
    
    logger.info("Initializing knowledge base with sample data...")
    
    # Sample knowledge base content
    kb_documents = [
        # Delivery Policy
        "We offer fast delivery within 30 minutes or your pizza is free! Delivery is available from 10 AM to 11 PM daily. We deliver within a 10km radius of our store.",
        
        # Refund Policy
        "Our refund policy allows full refunds within 24 hours of order placement if the pizza hasn't been delivered. For quality issues, contact us immediately and we'll replace or refund your order.",
        
        # Allergen Information
        "All our pizzas contain wheat (gluten) and dairy. Some toppings may contain nuts, soy, or eggs. Please inform us of allergies when ordering. We have a separate veg kitchen to avoid cross-contamination.",
        
        # Payment Methods
        "We accept cash on delivery, credit/debit cards, digital wallets (PayPal, Google Pay, Apple Pay), and cryptocurrency (Bitcoin, Ethereum). Payment is required before delivery confirmation.",
        
        # Order Tracking
        "Track your order in real-time! After placing an order, you'll receive an order ID. Use it to check status: Created → Confirmed → Preparing → Out for Delivery → Delivered. Updates are sent via SMS and app notifications.",
        
        # Opening Hours
        "We're open 7 days a week! Monday to Friday: 10 AM - 11 PM. Saturday and Sunday: 9 AM - 12 AM (midnight). We're closed on major holidays (Christmas, New Year's Day).",
        
        # Offers and Deals
        "Current offers: Buy 2 Large Pizzas, Get 1 Medium Free! Student discount: 15% off with valid ID. First-time customers get 10% off. Check our app for daily deals and promo codes.",
        
        # Complaints
        "For complaints or issues, contact our customer support at support@pizzaco.com or call 1-800-PIZZA-NOW. We respond within 2 hours. For urgent issues, use live chat on our website.",
        
        # Ingredients
        "We use 100% fresh ingredients sourced locally. Our dough is made fresh daily with organic flour. Cheese is imported Italian mozzarella. Vegetables are pesticide-free. Meats are halal-certified.",
        
        # Customization
        "Customize your pizza! Choose from 3 sauce options (tomato, white, BBQ), 5 cheese types, and 20+ toppings. Extra toppings are $1.50 each. Build your perfect pizza!",
        
        # Nutritional Information
        "Nutritional info available on request. Average medium pizza: 1200-1500 calories. Veggie options are lower in calories. Gluten-free crust available for +$3. Ask for our nutrition guide!",
        
        # Loyalty Program
        "Join our Pizza Rewards program! Earn 1 point per dollar spent. 100 points = $10 off. Birthday month rewards: Free dessert pizza! Refer a friend and both get 50 bonus points."
    ]
    
    # Metadata for each document
    kb_metadatas = [
        {"category": "Delivery", "title": "Delivery Policy", "source": "company_policy"},
        {"category": "Refunds", "title": "Refund Policy", "source": "company_policy"},
        {"category": "Allergies", "title": "Allergen Information", "source": "product_info"},
        {"category": "Payments", "title": "Payment Methods", "source": "company_policy"},
        {"category": "Order Tracking", "title": "How to Track Orders", "source": "user_guide"},
        {"category": "Opening Hours", "title": "Store Hours", "source": "company_info"},
        {"category": "Offers", "title": "Current Deals", "source": "marketing"},
        {"category": "Complaints", "title": "Customer Support", "source": "company_policy"},
        {"category": "Ingredients", "title": "Our Ingredients", "source": "product_info"},
        {"category": "Customization", "title": "Pizza Customization", "source": "product_info"},
        {"category": "Nutrition", "title": "Nutritional Information", "source": "product_info"},
        {"category": "Loyalty", "title": "Rewards Program", "source": "marketing"}
    ]
    
    # Generate IDs
    kb_ids = [f"kb_{i+1:03d}" for i in range(len(kb_documents))]
    
    # Add to vector store
    rag_tool.add_documents(kb_documents, kb_metadatas, kb_ids)
    
    logger.info(f"✅ Knowledge base initialized with {len(kb_documents)} documents")
