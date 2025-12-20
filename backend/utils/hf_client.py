"""
HuggingFace LLM Client with optional Groq and Google fallback support
"""
import os
import requests
import logging
import time
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class HuggingFaceLLM:
    """HuggingFace Inference API Client"""
    
    def __init__(self):
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 800, 
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """
        Generate text completion using HuggingFace API
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            max_retries: Number of retry attempts
            
        Returns:
            Generated text
        """
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("generated_text", "")
                    return str(result)
                
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    logger.warning(f"Model loading, retrying in {2 ** attempt}s...")
                    time.sleep(2 ** attempt)
                    continue
                
                elif response.status_code == 410:
                    # API endpoint deprecated - log warning but try to continue
                    logger.warning(f"HuggingFace API endpoint deprecated: {response.text}")
                    # Still try to continue in case it works
                    
                else:
                    logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    
            except requests.exceptions.Timeout:
                logger.error(f"Request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                    
            except Exception as e:
                logger.error(f"Error in HuggingFace generation: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                
        raise Exception("Failed to generate response from HuggingFace after retries")


class GroqLLM:
    """Groq API Client (Optional Fallback)"""
    
    def __init__(self):
        try:
            from groq import Groq
            self.api_key = os.getenv("GROQ_API_KEY")
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            self.client = Groq(api_key=self.api_key) if self.api_key else None
        except ImportError:
            logger.warning("Groq library not installed")
            self.client = None
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 800, 
        temperature: float = 0.7
    ) -> str:
        """Generate text using Groq API"""
        if not self.client:
            raise Exception("Groq client not initialized")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise


class GoogleLLM:
    """Google Generative AI Client (Optional Fallback)"""
    
    def __init__(self):
        try:
            import google.generativeai as genai
            self.api_key = os.getenv("GOOGLE_API_KEY")
            self.model_name = os.getenv("GOOGLE_MODEL", "gemini-pro")
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            else:
                self.model = None
        except ImportError:
            logger.warning("Google GenerativeAI library not installed")
            self.model = None
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 800, 
        temperature: float = 0.7
    ) -> str:
        """Generate text using Google Gemini API"""
        if not self.model:
            raise Exception("Google model not initialized")
        
        try:
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": temperature
            }
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            logger.error(f"Google generation error: {e}")
            raise


class MultiLLMClient:
    """
    Multi-provider LLM Client with fallback support
    Primary: HuggingFace
    Fallbacks: Groq, Google
    """
    
    def __init__(self):
        self.hf = HuggingFaceLLM()
        self.groq = GroqLLM()
        self.google = GoogleLLM()
        self.providers = ["huggingface", "groq", "google"]
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 800, 
        temperature: float = 0.7,
        preferred_provider: str = "huggingface"
    ) -> str:
        """
        Generate text with automatic fallback
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            preferred_provider: Preferred LLM provider
            
        Returns:
            Generated text
        """
        # Try preferred provider first
        providers_to_try = [preferred_provider] + [p for p in self.providers if p != preferred_provider]
        
        for provider in providers_to_try:
            try:
                logger.info(f"Trying LLM provider: {provider}")
                
                if provider == "huggingface":
                    return self.hf.generate(prompt, max_tokens, temperature)
                
                elif provider == "groq" and self.groq.client:
                    return self.groq.generate(prompt, max_tokens, temperature)
                
                elif provider == "google" and self.google.model:
                    return self.google.generate(prompt, max_tokens, temperature)
                
            except Exception as e:
                logger.error(f"Provider {provider} failed: {e}")
                continue
        
        raise Exception("All LLM providers failed to generate response")


# Global LLM client instance
llm_client = MultiLLMClient()


def get_llm_client() -> MultiLLMClient:
    """Get LLM client instance"""
    return llm_client


def generate_text(
    prompt: str, 
    max_tokens: int = 800, 
    temperature: float = 0.7,
    provider: str = "groq"  # Changed from "huggingface" to "groq"
) -> str:
    """Convenience function to generate text"""
    return llm_client.generate(prompt, max_tokens, temperature, provider)
