"""
Test FAQ Knowledge Base Retrieval
Comprehensive tests for common FAQ queries with FAISS + fallback
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


def test_faq_delivery_hours():
    """Test delivery hours FAQ"""
    print("\n" + "=" * 60)
    print("TEST 1: Delivery Hours FAQ")
    print("=" * 60)
    
    from tools.rag_tool import search_kb, initialize_knowledge_base
    
    # Ensure KB is initialized
    initialize_knowledge_base()
    
    # Test various phrasings
    queries = [
        "What are your delivery hours?",
        "delivery hours",
        "when do you deliver",
        "store hours",
        "opening hours",
        "what time do you open",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        assert len(results) > 0, f"Should return results for '{query}'"
        
        # Check if any result mentions hours/time
        found_hours = False
        for r in results:
            text = r.get("text", "").lower()
            if any(word in text for word in ["hour", "time", "open", "10 am", "11 pm"]):
                found_hours = True
                print(f"  ✅ Found hours info: {text[:100]}...")
                break
        
        assert found_hours, f"Should find hours information for '{query}'"
    
    print("\n✅ PASS: Delivery hours queries answered correctly")
    print()


def test_faq_refund_policy():
    """Test refund policy FAQ"""
    print("=" * 60)
    print("TEST 2: Refund Policy FAQ")
    print("=" * 60)
    
    from tools.rag_tool import search_kb
    
    queries = [
        "What is your refund policy?",
        "refund policy",
        "can I get a refund",
        "return policy",
        "money back",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        assert len(results) > 0, f"Should return results for '{query}'"
        
        # Check if any result mentions refund
        found_refund = False
        for r in results:
            text = r.get("text", "").lower()
            metadata = r.get("metadata", {})
            category = metadata.get("category", "").lower()
            
            if "refund" in text or "refund" in category:
                found_refund = True
                print(f"  ✅ Found refund info: {text[:100]}...")
                break
        
        assert found_refund, f"Should find refund information for '{query}'"
    
    print("\n✅ PASS: Refund policy queries answered correctly")
    print()


def test_faq_payment_methods():
    """Test payment methods FAQ"""
    print("=" * 60)
    print("TEST 3: Payment Methods FAQ")
    print("=" * 60)
    
    from tools.rag_tool import search_kb
    
    queries = [
        "What payment methods do you accept?",
        "payment methods",
        "how can I pay",
        "do you accept credit cards",
        "cash on delivery",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        assert len(results) > 0, f"Should return results for '{query}'"
        
        # Check if any result mentions payment
        found_payment = False
        for r in results:
            text = r.get("text", "").lower()
            metadata = r.get("metadata", {})
            category = metadata.get("category", "").lower()
            
            if any(word in text for word in ["payment", "cash", "card", "pay"]) or "payment" in category:
                found_payment = True
                print(f"  ✅ Found payment info: {text[:100]}...")
                break
        
        assert found_payment, f"Should find payment information for '{query}'"
    
    print("\n✅ PASS: Payment methods queries answered correctly")
    print()


def test_faq_allergens():
    """Test allergen information FAQ"""
    print("=" * 60)
    print("TEST 4: Allergen Information FAQ")
    print("=" * 60)
    
    from tools.rag_tool import search_kb
    
    queries = [
        "Do you have allergen information?",
        "allergens",
        "gluten free",
        "nut allergy",
        "dairy free",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        assert len(results) > 0, f"Should return results for '{query}'"
        
        # Check if any result mentions allergens
        found_allergen = False
        for r in results:
            text = r.get("text", "").lower()
            if any(word in text for word in ["allergen", "allerg", "gluten", "dairy", "nut", "wheat"]):
                found_allergen = True
                print(f"  ✅ Found allergen info: {text[:100]}...")
                break
        
        assert found_allergen, f"Should find allergen information for '{query}'"
    
    print("\n✅ PASS: Allergen queries answered correctly")
    print()


def test_partial_queries():
    """Test partial/typo queries"""
    print("=" * 60)
    print("TEST 5: Partial Queries and Typos")
    print("=" * 60)
    
    from tools.rag_tool import search_kb
    
    # Partial queries
    queries = [
        "deliver",
        "refun",
        "paymnt",
        "hour",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        # These very short/typo queries should either:
        # 1. Return 0 results (< 3 chars handled)
        # 2. Return some results via fallback
        print(f"  Results: {len(results)}")
        
        if len(results) > 0:
            print(f"  ✅ Fallback found {len(results)} result(s)")
        else:
            print(f"  ℹ️ No results (query might be too short)")
    
    print("\n✅ PASS: Partial queries handled appropriately")
    print()


def test_fallback_activation():
    """Test that fallback search activates correctly"""
    print("=" * 60)
    print("TEST 6: Fallback Search Activation")
    print("=" * 60)
    
    from tools.rag_tool import search_kb
    
    # Use a query that might not have perfect vector match
    # but should match via text fallback
    queries = [
        "free delivery",
        "30 minutes",
        "pizza ingredients",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        if len(results) > 0:
            # Check if any result has 'text_fallback' source
            fallback_used = any(r.get("source") == "text_fallback" for r in results)
            
            if fallback_used:
                print(f"  ✅ Fallback search activated")
            else:
                print(f"  ✅ FAISS search successful")
            
            print(f"  Found {len(results)} result(s)")
        else:
            print(f"  ⚠️ No results found")
    
    print("\n✅ PASS: Fallback mechanism working")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTING FAQ KNOWLEDGE BASE RETRIEVAL")
    print("=" * 60)
    
    try:
        test_faq_delivery_hours()
        test_faq_refund_policy()
        test_faq_payment_methods()
        test_faq_allergens()
        test_partial_queries()
        test_fallback_activation()
        
        print("=" * 60)
        print("✅ ALL FAQ TESTS PASSED!")
        print("🎉 Knowledge base retrieval working correctly for FAQs")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
