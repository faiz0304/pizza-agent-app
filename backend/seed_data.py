"""
Database Seed Script - Populate MongoDB with sample menu data
Run this script once to initialize the menu collection
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from utils.db import get_db


def seed_menu():
    """Seed the menu collection with sample pizza data"""
    
    menu_items = [
        {
            "id": "pepperoni_classic",
            "name": "Pepperoni Classic",
            "price": 12.99,
            "description": "Traditional pepperoni pizza with mozzarella cheese and our signature tomato sauce",
            "ingredients": ["pepperoni", "mozzarella", "tomato sauce", "pizza dough", "oregano"],
            "variants": {
                "small": 9.99,
                "medium": 12.99,
                "large": 15.99
            },
            "category": "non-veg",
            "tags": ["popular", "classic", "spicy"],
            "images": ["https://images.unsplash.com/photo-1628840042765-356cda07504e"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "margherita",
            "name": "Margherita",
            "price": 10.99,
            "description": "Simple and delicious with fresh mozzarella, basil, and tomato sauce",
            "ingredients": ["mozzarella", "fresh basil", "tomato sauce", "pizza dough", "olive oil"],
            "variants": {
                "small": 7.99,
                "medium": 10.99,
                "large": 13.99
            },
            "category": "veg",
            "tags": ["popular", "classic", "vegetarian"],
            "images": ["https://images.unsplash.com/photo-1604068549290-dea0e4a305ca"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "bbq_chicken",
            "name": "BBQ Chicken",
            "price": 14.99,
            "description": "Grilled chicken with BBQ sauce, red onions, and cilantro",
            "ingredients": ["grilled chicken", "bbq sauce", "red onions", "cilantro", "mozzarella", "pizza dough"],
            "variants": {
                "small": 11.99,
                "medium": 14.99,
                "large": 17.99
            },
            "category": "non-veg",
            "tags": ["popular", "bbq", "chicken"],
            "images": ["https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "veggie_supreme",
            "name": "Veggie Supreme",
            "price": 13.99,
            "description": "Loaded with bell peppers, mushrooms, onions, olives, and tomatoes",
            "ingredients": ["bell peppers", "mushrooms", "onions", "black olives", "tomatoes", "mozzarella", "pizza dough"],
            "variants": {
                "small": 10.99,
                "medium": 13.99,
                "large": 16.99
            },
            "category": "veg",
            "tags": ["vegetarian", "healthy", "loaded"],
            "images": ["https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "meat_lovers",
            "name": "Meat Lovers",
            "price": 16.99,
            "description": "Loaded with pepperoni, sausage, bacon, and ham",
            "ingredients": ["pepperoni", "italian sausage", "bacon", "ham", "mozzarella", "tomato sauce", "pizza dough"],
            "variants": {
                "small": 13.99,
                "medium": 16.99,
                "large": 19.99
            },
            "category": "non-veg",
            "tags": ["popular", "meat", "protein-packed"],
            "images": ["https://images.unsplash.com/photo-1534308983496-4fabb1a015ee"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "four_cheese",
            "name": "Four Cheese",
            "price": 14.99,
            "description": "A cheese lover's dream with mozzarella, parmesan, gorgonzola, and provolone",
            "ingredients": ["mozzarella", "parmesan", "gorgonzola", "provolone", "white sauce", "pizza dough"],
            "variants": {
                "small": 11.99,
                "medium": 14.99,
                "large": 17.99
            },
            "category": "veg",
            "tags": ["cheese", "creamy", "gourmet"],
            "images": ["https://images.unsplash.com/photo-1574071318508-1cdbab80d002"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "spicy_devil",
            "name": "Spicy Devil",
            "price": 15.99,
            "description": "Extra spicy with jalapeños, hot sauce, pepperoni, and red chili flakes",
            "ingredients": ["jalapeños", "hot sauce", "pepperoni", "red chili flakes", "mozzarella", "tomato sauce", "pizza dough"],
            "variants": {
                "small": 12.99,
                "medium": 15.99,
                "large": 18.99
            },
            "category": "non-veg",
            "tags": ["spicy", "hot", "extreme"],
            "images": ["https://images.unsplash.com/photo-1593560708920-61dd98c46a4e"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "hawaiian",
            "name": "Hawaiian Paradise",
            "price": 13.99,
            "description": "Ham and pineapple with mozzarella on a tomato base - a tropical favorite",
            "ingredients": ["ham", "pineapple", "mozzarella", "tomato sauce", "pizza dough"],
            "variants": {
                "small": 10.99,
                "medium": 13.99,
                "large": 16.99
            },
            "category": "non-veg",
            "tags": ["tropical", "sweet_savory"],
            "images": ["https://images.unsplash.com/photo-1565299585323-38d6b0865b47"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "mushroom_truffle",
            "name": "Mushroom & Truffle",
            "price": 17.99,
            "description": "Gourmet pizza with mixed mushrooms, truffle oil, and parmesan",
            "ingredients": ["mixed mushrooms", "truffle oil", "parmesan", "mozzarella", "white sauce", "pizza dough", "arugula"],
            "variants": {
                "small": 14.99,
                "medium": 17.99,
                "large": 20.99
            },
            "category": "veg",
            "tags": ["gourmet", "luxury", "earthy"],
            "images": ["https://images.unsplash.com/photo-1574071318508-1cdbab80d002"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "buffalo_chicken",
            "name": "Buffalo Chicken",
            "price": 15.99,
            "description": "Spicy buffalo chicken with ranch dressing, celery, and blue cheese",
            "ingredients": ["buffalo chicken", "ranch dressing", "celery", "blue cheese", "mozzarella", "pizza dough"],
            "variants": {
                "small": 12.99,
                "medium": 15.99,
                "large": 18.99
            },
            "category": "non-veg",
            "tags": ["spicy", "chicken", "ranch"],
            "images": ["https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Connect to database
    db = get_db()
    db.connect()
    
    # Check if menu already has data
    existing_count = db.get_collection("menu").count_documents({})
    if existing_count > 0:
        print(f"WARNING: Menu collection already has {existing_count} items")
        response = input("Do you want to clear and reseed? (yes/no): ")
        if response.lower() != "yes":
            print("Seed cancelled")
            return
        else:
            db.get_collection("menu").delete_many({})
            print("Cleared existing menu data")
    
    # Insert menu items
    print(f"Inserting {len(menu_items)} menu items...")
    for item in menu_items:
        db.insert_menu_item(item)
        print(f"Added: {item['name']}")
    
    print(f"\nSuccessfully seeded {len(menu_items)} menu items!")
    
    db.disconnect()


if __name__ == "__main__":
    print("=" * 50)
    print("Pizza Menu Seed Script")
    print("=" * 50)
    seed_menu()
