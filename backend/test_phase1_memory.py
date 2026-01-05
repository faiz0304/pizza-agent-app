"""
Test script for Phase 1: Short-Term Memory Enhancement
Tests structured session state, compression, and context generation
"""
import sys
sys.path.insert(0, 'D:\\Antigravity_pizza_agent\\pizza-agent-app\\backend')

from utils.memory import ConversationMemory

def test_structured_memory():
    """Test structured memory features"""
    print("🧪 Testing Short-Term Memory Enhancement...")
    print("=" * 60)
    
    # Create memory instance
    memory = ConversationMemory()
    user_id = "test_user_123"
    
    # Simulate conversation
    print("\n1️⃣ Simulating conversation...")
    memory.add_message(user_id, "user", "Salaam, mujhe pizza dikhao")
    memory.add_message(user_id, "assistant", "Sure! Here are our pizzas...")
    memory.add_message(user_id, "user", "I want 2 large pepperoni pizzas")
    memory.add_message(user_id, "assistant", "Great choice! Should I confirm?")
    memory.add_message(user_id, "user", "haan book karo")
    
    # Test compression
    print("\n2️⃣ Testing history compression...")
    compressed = memory.compress_history(user_id)
    print(f"✅ Compressed state: {compressed}")
    
    # Verify intents detected
    assert "create_order" in compressed["recent_intents"], "Should detect create_order intent"
    assert "confirmation" in compressed["recent_intents"], "Should detect confirmation intent"
    print(f"✅ Intents detected: {compressed['recent_intents']}")
    
    # Verify entities extracted
    entities = compressed["entities"]
    assert "pepperoni" in entities["mentioned_pizzas"], "Should extract pepperoni"
    assert 2 in entities["quantities"], "Should extract quantity 2"
    assert "large" in entities["preferences"], "Should extract large size"
    print(f"✅ Entities extracted: Pizzas={entities['mentioned_pizzas']}, Qty={entities['quantities']}, Prefs={entities['preferences']}")
    
    # Verify language detection
    assert compressed["language_hint"] == "roman_urdu", "Should detect Roman Urdu"
    print(f"✅ Language detected: {compressed['language_hint']}")
    
    # Test context generation
    print("\n3️⃣ Testing context generation for LLM...")
    context = memory.get_context_for_prompt(user_id, include_raw_history=False)
    print(f"✅ Compact context:\n{context}")
    
    # Verify token efficiency
    raw_history_length = sum(len(msg["content"]) for msg in memory.get_history(user_id))
    context_length = len(context)
    reduction = ((raw_history_length - context_length) / raw_history_length) * 100
    print(f"\n📊 Token Efficiency:")
    print(f"  Raw history: ~{raw_history_length} chars")
    print(f"  Compressed context: ~{context_length} chars")
    print(f"  Reduction: ~{reduction:.1f}%")
    
    # Test pending order tracking
    print("\n4️⃣ Testing pending order integration...")
    memory.set_pending_order(user_id, {
        "items": [{"name": "Pepperoni", "qty": 2}]
    })
    memory.compress_history(user_id)  # Recompress
    context_with_pending = memory.get_context_for_prompt(user_id)
    assert "PENDING ORDER" in context_with_pending, "Should show pending order in context"
    print(f"✅ Pending order reflected in context")
    
    # Test stats
    print("\n5️⃣ Checking memory statistics...")
    stats = memory.get_stats()
    print(f"✅ Stats: {stats}")
    assert stats["active_sessions"] == 1, "Should have 1 active session"
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("🎉 Phase 1: Short-Term Memory Enhancement is working correctly!")
    
    return True

if __name__ == "__main__":
    try:
        test_structured_memory()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
