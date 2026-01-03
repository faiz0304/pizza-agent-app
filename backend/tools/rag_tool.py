"""
RAG Tool - Knowledge Base Search using FAISS Vector Store
"""
import os
import logging
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import faiss

from utils.embeddings import embed_text

load_dotenv()

logger = logging.getLogger(__name__)


class RAGSearchTool:
    """
    Knowledge Base Search Tool using FAISS
    Performs semantic search over customer support knowledge base
    """
    
    def __init__(self):
        self.persist_dir = os.getenv("FAISS_PERSIST_DIR", "./faiss_db")
        self.index_file = os.path.join(self.persist_dir, "index.faiss")
        self.metadata_file = os.path.join(self.persist_dir, "metadata.pkl")
        self.index = None
        self.documents = []
        self.metadatas = []
        self.ids = []
        self.dimension = 768  # Default embedding dimension (sentence-transformers)
        self._initialize_faiss()
    
    def _initialize_faiss(self):
        """Initialize FAISS index and load existing data if available"""
        try:
            # Create persist directory if it doesn't exist
            os.makedirs(self.persist_dir, exist_ok=True)
            
            # Try to load existing index
            if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
                self._load_index()
                logger.info(f"✅ FAISS index loaded from disk")
                logger.info(f"Index count: {len(self.documents)} documents")
            else:
                # Create new index
                self.index = faiss.IndexFlatL2(self.dimension)
                logger.info(f"✅ FAISS index initialized (new)")
                logger.info(f"Index count: 0 documents")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize FAISS: {e}")
            raise
    
    def _load_index(self):
        """Load FAISS index and metadata from disk"""
        try:
            # Load FAISS index
            self.index = faiss.read_index(self.index_file)
            
            # Load metadata
            with open(self.metadata_file, 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.metadatas = data['metadatas']
                self.ids = data['ids']
                self.dimension = data.get('dimension', 768)
            
            logger.info(f"Loaded {len(self.documents)} documents from disk")
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            # Fallback to new index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []
            self.metadatas = []
            self.ids = []
    
    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_file)
            
            # Save metadata
            with open(self.metadata_file, 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'metadatas': self.metadatas,
                    'ids': self.ids,
                    'dimension': self.dimension
                }, f)
            
            logger.info(f"Saved {len(self.documents)} documents to disk")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
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
            embeddings = np.array([embed_text(doc) for doc in documents], dtype='float32')
            
            # Add to FAISS index
            self.index.add(embeddings)
            
            # Store documents and metadata
            self.documents.extend(documents)
            self.metadatas.extend(metadatas)
            self.ids.extend(ids)
            
            # Save to disk
            self._save_index()
            
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
            
            # Handle empty index
            if len(self.documents) == 0:
                logger.warning("Knowledge base is empty")
                return []
            
            # Generate query embedding
            query_embedding = np.array([embed_text(query)], dtype='float32')
            
            # Search in FAISS
            top_k = min(top_k, len(self.documents))  # Don't request more than we have
            distances, indices = self.index.search(query_embedding, top_k)
            
            # Format results
            formatted_results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.documents):  # Valid index
                    formatted_results.append({
                        "text": self.documents[idx],
                        "metadata": self.metadatas[idx] if idx < len(self.metadatas) else {},
                        "score": float(distance),  # L2 distance (lower is better)
                        "id": self.ids[idx] if idx < len(self.ids) else None
                    })
            
            logger.info(f"Found {len(formatted_results)} results for query: '{query[:50]}...'")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            count = len(self.documents)
            return {
                "collection_name": "faiss_knowledge_base",
                "document_count": count,
                "persist_dir": self.persist_dir,
                "index_dimension": self.dimension
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def count(self) -> int:
        """Get document count in the knowledge base"""
        return len(self.documents)


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
    if rag_tool.count() > 0:
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
        "Join our Pizza Rewards program! Earn 1 point per dollar spent. 100 points = $10 off. Birthday month rewards: Free dessert pizza! Refer a friend and both get 50 bonus points!"
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
