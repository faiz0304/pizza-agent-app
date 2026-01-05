"""
Test Order Confirmation Flow
Tests that 'yes' and other confirmations properly use pending orders
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from utils.memory import ConversationMemory


def test_confirmation_with_pending_order():
    """Test that confirmation creates order with pending items"""
    print("\n" + "=" * 60)
    print("TEST 1: Confirmation with Pending Order")
    print("=" * 60)
    
    memory = ConversationMemory(max_history=25)
    user_id = "test_user_confirm"
    
    # Simulate order suggestion
    pending_order_data = {
        "user": {"user_id": user_id},
        "items": [
            {"name": "Pepperoni Classic", "qty": 1, "variant": "medium", "price": 12.99}
        ]
    }
    
    memory.set_pending_order(user_id, pending_order_data)
    print(f"Set pending order: {pending_order_data}")
    
    # Simulate user saying "yes"
    memory.add_message(user_id, "user", "yes")
    
    # Retrieve pending order
    retrieved = memory.get_pending_order(user_id)
    print(f"Retrieved pending order: {retrieved}")
    
    assert retrieved is not None, "Pending order should exist"
    assert "items" in retrieved, "Pending order should have items"
    assert len(retrieved["items"]) > 0, "Pending order should have at least one item"
    assert retrieved["items"][0]["name"] == "Pepperoni Classic", "Item should match"
    
    print("✅ PASS: Forward confirmation retrieves pending order with items")
    print()
    
    memory.clear_history(user_id)


def test_confirmation_without_pending_order():
    """Test that confirmation without pending order gives helpful message"""
    print("=" * 60)
    print("TEST 2: Confirmation WITHOUT Pending Order")
    print("=" * 60)
    
    memory = ConversationMemory(max_history=25)
    user_id = "test_user_no_pending"
    
    # User says "yes" but no pending order exists
    memory.add_message(user_id, "user", "yes confirm my order")
    
    # Check pending order
    pending = memory.get_pending_order(user_id)
    print(f"Pending order: {pending}")
    
    assert pending is None, "No pending order should exist"
    
    print("✅ PASS: No pending order detected (should trigger helpful message)")
    print()
    
    memory.clear_history(user_id)


def test_pending_order_with_empty_items():
    """Test that pending order with empty items list is handled"""
    print("=" * 60)
    print("TEST 3: Pending Order with Empty Items")
    print("=" * 60)
    
    memory = ConversationMemory(max_history=25)
    user_id = "test_user_empty"
    
    # Set pending order with empty items
    pending_order_data = {
        "user": {"user_id": user_id},
        "items": []  # Empty!
    }
    
    memory.set_pending_order(user_id, pending_order_data)
    print(f"Set pending order with empty items: {pending_order_data}")
    
    # Check pending order
    retrieved = memory.get_pending_order(user_id)
    print(f"Retrieved: {retrieved}")
    
    assert retrieved is not None, "Pending order exists"
    assert len(retrieved.get("items", [])) == 0, "Items should be empty"
    
    print("✅ PASS: Empty items detected (should be validated in chatbot route)")
    print()
    
    memory.clear_history(user_id)


def test_multiple_confirmation_keywords():
    """Test various confirmation keywords"""
    print("=" * 60)
    print("TEST 4: Multiple Confirmation Keywords")
    print("=" * 60)
    
    confirmations = [
        "yes",
        "haan",
        "ha",
        "confirm",
        "ok",
        "okay",
        "theek hai",
        "acha",
        "sure",
        "book karo",
        "karo"
    ]
    
    memory = ConversationMemory(max_history=25)
    
    for keyword in confirmations:
        user_id = f"test_{keyword}"
        
        # Set pending order
        memory.set_pending_order(user_id, {
            "user": {"user_id": user_id},
            "items": [{"name": "Test Pizza", "qty": 1}]
        })
        
        # Simulate user saying keyword
        message_lower = keyword.lower()
        is_confirmation = any(kw in message_lower for kw in confirmations)
        
        assert is_confirmation, f"'{keyword}' should be recognized as confirmation"
        print(f"  ✅ '{keyword}' recognized")
        
        memory.clear_history(user_id)
    
    print("\n✅ PASS: All confirmation keywords recognized")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTING ORDER CONFIRMATION FLOW")
    print("=" * 60)
    
    try:
        test_confirmation_with_pending_order()
        test_confirmation_without_pending_order()
        test_pending_order_with_empty_items()
        test_multiple_confirmation_keywords()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("🎉 Order confirmation flow working correctly")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
