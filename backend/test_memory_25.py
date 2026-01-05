"""
Test 25-Message Memory Enhancement
Tests memory limit, MongoDB persistence, session expiry, and multi-user isolation
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from utils.memory import ConversationMemory
from utils.db import get_db
from datetime import datetime, timedelta


def test_25_message_limit():
    """Test that memory correctly limits to 25 messages"""
    print("\n" + "=" * 60)
    print("TEST 1: 25-Message Limit")
    print("=" * 60)
    
    memory = ConversationMemory(max_history=25)
    user_id = "test_user_limit"
    
    # Add 30 messages
    print(f"Adding 30 messages...")
    for i in range(30):
        role = "user" if i % 2 == 0 else "assistant"
        memory.add_message(user_id, role, f"Message {i+1}")
    
    # Check that only last 25 are retained
    history = memory.get_history(user_id)
    print(f"Messages in memory: {len(history)}")
    
    assert len(history) == 25, f"Expected 25 messages, got {len(history)}"
    assert history[0]["content"] == "Message 6", f"Expected first message to be 'Message 6', got '{history[0]['content']}'"
    assert history[-1]["content"] == "Message 30", f"Expected last message to be 'Message 30', got '{history[-1]['content']}'"
    
    print("✅ PASS: Memory correctly limited to 25 messages")
    print()
    
    memory.clear_history(user_id)


def test_mongodb_persistence():
    """Test MongoDB session persistence across memory instances"""
    print("=" * 60)
    print("TEST 2: MongoDB Persistence")
    print("=" * 60)
    
    db = get_db()
    user_id = "test_user_persist"
    
    # Create first memory instance and add messages
    print("Creating first memory instance...")
    memory1 = ConversationMemory(max_history=25, db=db)
    memory1.add_message(user_id, "user", "Hello")
    memory1.add_message(user_id, "assistant", "Hi there!")
    memory1.add_message(user_id, "user", "How are you?")
    
    print(f"Added 3 messages to memory1")
    
    # Create second memory instance (simulates server restart)
    print("Creating second memory instance (simulating restart)...")
    memory2 = ConversationMemory(max_history=25, db=db)
    
    # Load from database
    history = memory2.get_history(user_id)
    print(f"Loaded {len(history)} messages from database")
    
    assert len(history) == 3, f"Expected 3 messages, got {len(history)}"
    assert history[0]["content"] == "Hello", "First message should be 'Hello'"
    assert history[-1]["content"] == "How are you?", "Last message should be 'How are you?'"
    
    print("✅ PASS: Session persists across memory instances")
    print()
    
    # Cleanup
    db.delete_chat_session(user_id)


def test_session_expiry():
    """Test that expired sessions are cleaned up"""
    print("=" * 60)
    print("TEST 3: Session Expiry Cleanup")
    print("=" * 60)
    
    db = get_db()
    user_id = "test_user_expiry"
    
    # Create session with short expiry
    memory = ConversationMemory(max_history=25, expiry_minutes=0, db=db)  # Expire immediately
    memory.add_message(user_id, "user", "Test message")
    
    print("Created session with 0-minute expiry")
    
    # Manually set expiry to past
    from datetime import datetime
    db.save_chat_session(
        user_id=user_id,
        messages=[{"role": "user", "content": "Test"}],
        session_state={},
        expires_at=datetime.utcnow() - timedelta(minutes=1)  # Already expired
    )
    
    print("Set expiry to past")
    
    # Try to load - should return None for expired session
    session = db.get_chat_session(user_id)
    
    assert session is None, "Expired session should not be retrievable"
    print("✅ PASS: Expired sessions are not retrieved")
    
    # Test cleanup
    count = db.cleanup_expired_sessions()
    print(f"Cleaned up {count} expired session(s)")
    
    print("✅ PASS: Session expiry and cleanup work correctly")
    print()


def test_multi_user_isolation():
    """Test that sessions don't mix between users"""
    print("=" * 60)
    print("TEST 4: Multi-User Session Isolation")
    print("=" * 60)
    
    memory = ConversationMemory(max_history=25)
    
    # Add messages for user 1
    memory.add_message("user1", "user", "User 1 message 1")
    memory.add_message("user1", "assistant", "User 1 response 1")
    
    # Add messages for user 2
    memory.add_message("user2", "user", "User 2 message 1")
    memory.add_message("user2", "assistant", "User 2 response 1")
    
    # Add messages for user 3
    memory.add_message("user3", "user", "User 3 message 1")
    
    print("Added messages for 3 users")
    
    # Check isolation
    history1 = memory.get_history("user1")
    history2 = memory.get_history("user2")
    history3 = memory.get_history("user3")
    
    print(f"User1: {len(history1)} messages, User2: {len(history2)} messages, User3: {len(history3)} messages")
    
    assert len(history1) == 2, f"User1 should have 2 messages, got {len(history1)}"
    assert len(history2) == 2, f"User2 should have 2 messages, got {len(history2)}"
    assert len(history3) == 1, f"User3 should have 1 message, got {len(history3)}"
    
    assert history1[0]["content"] == "User 1 message 1", "User1 messages should be isolated"
    assert history2[0]["content"] == "User 2 message 1", "User2 messages should be isolated"
    assert history3[0]["content"] == "User 3 message 1", "User3 messages should be isolated"
    
    print("✅ PASS: Sessions are properly isolated between users")
    print()
    
    # Cleanup
    memory.clear_history("user1")
    memory.clear_history("user2")
    memory.clear_history("user3")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTING 25-MESSAGE MEMORY ENHANCEMENT")
    print("=" * 60)
    
    try:
        test_25_message_limit()
        test_mongodb_persistence()
        test_session_expiry()
        test_multi_user_isolation()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("🎉 25-message memory system working correctly")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
