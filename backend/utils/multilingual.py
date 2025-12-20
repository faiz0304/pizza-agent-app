"""
Multilingual Support - Roman Urdu/Hindi detection and translation helpers
"""
import re
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


# Common Roman Urdu/Hindi words and phrases for detection
ROMAN_URDU_HINDI_PATTERNS = [
    # Greetings
    r'\b(salaam|salam|namaste|namaskar|kya hal|kaisay|kaisi|kaise)\b',
    
    # Common words
    r'\b(acha|achchha|theek|thik|haan|han|nahi|nai|kya|kyun|kab|kahan|kaise)\b',
    
    # Pizza related
    r'\b(pizza|khana|order|delivery|bill|paisa|price|kitna|kitne)\b',
    
    # Action words
    r'\b(chahiye|chahta|chahti|dikhao|batao|dijiye|karna|karo|lena|lelo)\b',
    
    # Numbers in words
    r'\b(ek|do|teen|char|panch|paanch|sau|hazaar)\b'
]

COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in ROMAN_URDU_HINDI_PATTERNS]


def detect_roman_urdu_hindi(text: str) -> bool:
    """
    Detect if text contains Roman Urdu or Roman Hindi
    
    Args:
        text: Input text to check
        
    Returns:
        True if Roman Urdu/Hindi detected
    """
    if not text:
        return False
    
    # Check against patterns
    matches = 0
    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            matches += 1
    
    # If 2+ patterns match, likely Roman Urdu/Hindi
    is_roman_urdu_hindi = matches >= 2
    
    if is_roman_urdu_hindi:
        logger.info(f"Detected Roman Urdu/Hindi input: {text[:50]}...")
    
    return is_roman_urdu_hindi


def get_multilingual_prompt_prefix(text: str) -> str:
    """
    Get appropriate prompt prefix for multilingual support
    
    Args:
        text: User input text
        
    Returns:
        Prompt prefix string
    """
    if detect_roman_urdu_hindi(text):
        return """
IMPORTANT: The user is communicating in Roman Urdu/Hindi (Urdu/Hindi written in English/Roman script).
Understand their message and respond in a way that's natural for them.
You can respond in English, but use simple, friendly language that's easy to understand.
Consider using some common Urdu/Hindi words if appropriate (like "acha", "theek hai", "kya chahiye").

"""
    return ""


# Common translations for reference
COMMON_TRANSLATIONS = {
    # Greetings
    "salaam": "hello/peace be upon you",
    "namaste": "hello/greetings",
    "kya hal": "how are you",
    
    # Questions
    "kya": "what",
    "kyun": "why",
    "kab": "when",
    "kahan": "where",
    "kaise": "how",
    "kitna": "how much",
    
    # Responses
    "haan": "yes",
    "nahi": "no",
    "acha": "good/okay",
    "theek": "fine/okay",
    
    # Actions
    "chahiye": "want/need",
    "dikhao": "show me",
    "batao": "tell me",
    "karo": "do it",
    "lelo": "take it",
    
    # Numbers
    "ek": "one",
    "do": "two",
    "teen": "three",
    "char": "four",
    "panch": "five"
}


def get_translation_hint(word: str) -> Optional[str]:
    """
    Get English translation hint for a Roman Urdu/Hindi word
    
    Args:
        word: Roman Urdu/Hindi word
        
    Returns:
        English translation or None
    """
    return COMMON_TRANSLATIONS.get(word.lower())
