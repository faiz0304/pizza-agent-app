"""
Embedding generation utilities using HuggingFace sentence-transformers
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generate embeddings using HuggingFace sentence-transformers"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        
        Args:
            model_name: HuggingFace model name for embeddings
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"✅ Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text string
            
        Returns:
            List of floats representing the embedding vector
        """
        if not self.model:
            raise Exception("Embedding model not loaded")
        
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input text strings
            
        Returns:
            List of embedding vectors
        """
        if not self.model:
            raise Exception("Embedding model not loaded")
        
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False, show_progress_bar=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors"""
        if not self.model:
            raise Exception("Embedding model not loaded")
        return self.model.get_sentence_embedding_dimension()


# Global embedding generator instance
embedding_generator = EmbeddingGenerator()


def get_embedding_generator() -> EmbeddingGenerator:
    """Get embedding generator instance"""
    return embedding_generator


def embed_text(text: str) -> List[float]:
    """Convenience function to embed a single text"""
    return embedding_generator.embed_text(text)


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Convenience function to embed multiple texts"""
    return embedding_generator.embed_batch(texts)
