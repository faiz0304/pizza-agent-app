"""
Recommend Tool - AI-powered pizza recommendations based on user preferences
"""
import logging
from typing import List, Dict, Any, Union

from utils.hf_client import generate_text
from utils.db import get_db
from tools.menu_tool import get_all_menu_items, filter_menu_by_category, filter_menu_by_tags

logger = logging.getLogger(__name__)


def recommend_pizza(preferences: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Recommend pizzas based on user preferences using LLM and menu matching
    
    Args:
        preferences: String or dict describing user preferences
                    Examples: "spicy and cheesy", {"taste": "spicy", "diet": "veg"}
        
    Returns:
        List of recommended menu items with reasoning
    """
    try:
        # Convert preferences to string if dict
        if isinstance(preferences, dict):
            pref_parts = []
            for key, value in preferences.items():
                pref_parts.append(f"{key}: {value}")
            pref_string = ", ".join(pref_parts)
        else:
            pref_string = str(preferences)
        
        logger.info(f"Generating recommendations for preferences: {pref_string}")
        
        # Get all menu items
        menu_items = get_all_menu_items()
        
        if not menu_items:
            logger.warning("No menu items available for recommendations")
            return []
        
        # Build a simplified menu description for LLM
        menu_summary = []
        for idx, item in enumerate(menu_items[:20], 1):  # Limit to 20 for token efficiency
            summary = f"{idx}. {item['name']} - {item.get('category', 'pizza')}, {item.get('description', '')[:100]}"
            if item.get('tags'):
                summary += f" (Tags: {', '.join(item['tags'][:3])})"
            menu_summary.append(summary)
        
        menu_text = "\n".join(menu_summary)
        
        # Create prompt for LLM
        prompt = f"""You are a pizza recommendation expert. Based on the customer's preferences, recommend the TOP 3 pizzas from the menu below.

Customer Preferences: {pref_string}

Available Menu:
{menu_text}

Instructions:
1. Analyze the preferences carefully
2. Match them with the menu items
3. Return ONLY a JSON array with exactly 3 recommendations
4. Each recommendation should have: "name", "reason" (1 sentence why it matches)

Format your response as valid JSON only:
[
  {{"name": "Pizza Name", "reason": "Why this matches the preference"}},
  {{"name": "Pizza Name", "reason": "Why this matches the preference"}},
  {{"name": "Pizza Name", "reason": "Why this matches the preference"}}
]

JSON Response:"""

        # Get LLM recommendation
        try:
            llm_response = generate_text(prompt, max_tokens=400, temperature=0.7)
            
            # Try to parse JSON from response
            import json
            import re
            
            # Extract JSON from response (handle cases where LLM adds extra text)
            json_match = re.search(r'\[.*\]', llm_response, re.DOTALL)
            if json_match:
                recommendations_data = json.loads(json_match.group())
            else:
                raise ValueError("No JSON array found in LLM response")
            
            # Match recommended names with actual menu items
            recommended_items = []
            for rec in recommendations_data[:3]:  # Limit to 3
                rec_name = rec.get("name", "")
                reason = rec.get("reason", "")
                
                # Find matching menu item
                matching_item = None
                for item in menu_items:
                    if rec_name.lower() in item["name"].lower() or item["name"].lower() in rec_name.lower():
                        matching_item = item.copy()
                        break
                
                if matching_item:
                    matching_item["recommendation_reason"] = reason
                    matching_item.pop('_id', None)
                    recommended_items.append(matching_item)
            
            if recommended_items:
                logger.info(f"✅ Generated {len(recommended_items)} recommendations")
                return recommended_items
            
        except Exception as llm_error:
            logger.error(f"LLM recommendation failed: {llm_error}, falling back to rule-based")
        
        # Fallback: Rule-based recommendation if LLM fails
        logger.info("Using fallback rule-based recommendation")
        return _fallback_recommendation(pref_string, menu_items)
        
    except Exception as e:
        logger.error(f"❌ Error generating recommendations: {e}")
        return []


def _fallback_recommendation(preferences: str, menu_items: List[Dict]) -> List[Dict]:
    """
    Fallback rule-based recommendation when LLM fails
    """
    pref_lower = preferences.lower()
    scored_items = []
    
    for item in menu_items:
        score = 0
        
        # Check category match
        if "veg" in pref_lower and item.get("category") == "veg":
            score += 3
        if "non-veg" in pref_lower and item.get("category") == "non-veg":
            score += 3
        
        # Check tags match
        tags = item.get("tags", [])
        if "spicy" in pref_lower and "spicy" in tags:
            score += 2
        if "cheese" in pref_lower and "cheese" in tags:
            score += 2
        if "popular" in tags:
            score += 1
        
        # Check description/name match
        item_text = (item.get("name", "") + " " + item.get("description", "")).lower()
        for keyword in ["spicy", "cheese", "bbq", "meat", "veggie", "classic"]:
            if keyword in pref_lower and keyword in item_text:
                score += 1
        
        scored_items.append((score, item))
    
    # Sort by score and take top 3
    scored_items.sort(key=lambda x: x[0], reverse=True)
    top_recommendations = [item for score, item in scored_items[:3]]
    
    # Add simple reasons
    for item in top_recommendations:
        item["recommendation_reason"] = f"Matches your preference for {preferences}"
        item.pop('_id', None)
    
    return top_recommendations
