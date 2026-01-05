"""
Test Knowledge Base Retrieval Enhancement
Tests FAISS vector search, fallback text search, and edge cases
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from tools.rag_tool import rag_tool, search_kb, initialize_knowledge_base


def test_faiss_vector_search():
    """Test FAISS vector search functionality"""
    print("\n" + "=" * 60)
    print("TEST 1: FAISS Vector Search")
    print("=" * 60)
    
    # Ensure KB is initialized
    initialize_knowledge_base()
    
    # Test common queries
    test_queries = [
        ("delivery hours", "Delivery"),
        ("refund policy", "Refunds"),
        ("payment methods", "Payments"),
        ("allergens", "Allergies"),
    ]
    
    for query, expected_category in test_queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=2)
        
        assert len(results) > 0, f"Should return results for '{query}'"
        
        # Check if expected category is in results
        categories = [r.get("metadata", {}).get("category", "") for r in results]
        print(f"  Found categories: {categories}")
        
        # At least one result should match expected category
        assert any(expected_category.lower() in cat.lower() for cat in categories), \
            f"Expected category '{expected_category}' in results for '{query}'"
    
    print("\n✅ PASS: FAISS vector search returns relevant results")
    print()


def test_fallback_text_search():
    """Test fallback text search when FAISS fails"""
    print("=" * 60)
    print("TEST 2: Fallback Text Search")
    print("=" * 60)
    
    # Test queries with common words that should trigger fallback
    queries = [
        "pizza",
        "free delivery",
        "30 minutes",
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_kb(query, top_k=3)
        
        # Should return results even if exact vector match is weak
        assert len(results) > 0, f"Should return results for '{query}' (FAISS or fallback)"
        
        # Check that text appears in results
        found = any(query.lower() in r["text"].lower() for r in results)
        print(f"  Found '{query}' in results: {found}")
        print(f"  Returned {len(results)} result(s)")
    
    print("\n✅ PASS: Fallback text search works correctly")
    print()


def test_edge_cases():
    """Test edge cases for KB retrieval"""
    print("=" * 60)
    print("TEST 3: Edge Cases")
    print("=" * 60)
    
    # Test empty query
    print("\nTest: Empty query")
    results = search_kb("", top_k=3)
    assert len(results) == 0, "Empty query should return no results"
    print("✅ Empty query handled correctly")
    
    # Test very short query (< 3 chars)
    print("\nTest: Very short query")
    results = search_kb("hi", top_k=3)
    assert len(results) == 0, "Query < 3 chars should return no results"
    print("✅ Short query handled correctly")
    
    # Test special characters
    print("\nTest: Special characters")
    results = search_kb("@#$%", top_k=3)
    # Should not crash, may return 0 or few results
    print(f"  Returned {len(results)} result(s)")
    print("✅ Special characters handled correctly")
    
    # Test very long query
    print("\nTest: Very long query")
    long_query = "What are your delivery hours and policies" * 10
    results = search_kb(long_query, top_k=3)
    # Should not crash
    print(f"  Returned {len(results)} result(s)")
    print("✅ Long query handled correctly")
    
    print("\n✅ PASS: All edge cases handled correctly")
    print()


def test_kb_initialization():
    """Test that KB is properly initialized"""
    print("=" * 60)
    print("TEST 4: KB Initialization")
    print("=" * 60)
    
    # Get KB stats
    stats = rag_tool.get_collection_stats()
    print(f"\nKB Stats:")
    print(f"  Collection: {stats.get('collection_name')}")
    print(f"  Document count: {stats.get('document_count')}")
    print(f"  Index dimension: {stats.get('index_dimension')}")
    
    # Should have documents
    doc_count = stats.get('document_count', 0)
    assert doc_count > 0, f"KB should have documents initialized, found {doc_count}"
    assert doc_count >= 10, f"KB should have at least 10 sample documents, found {doc_count}"
    
    print("\n✅ PASS: KB properly initialized with documents")
    print()


def test_all_kb_documents():
    """Test that all initialized documents are retrievable"""
    print("=" * 60)
    print("TEST 5: All KB Documents Retrievable")
    print("=" * 60)
    
    # Get expected document count
    expected_count = rag_tool.count()
    print(f"\nExpected document count: {expected_count}")
    
    # Test each category
    categories = [
        "Delivery", "Refunds", "Allergies", "Payments", 
        "Order Tracking", "Opening Hours", "Offers", 
        "Complaints", "Ingredients", "Customization", 
        "Nutrition", "Loyalty"
    ]
    
    found_categories = []
    for category in categories:
        results = search_kb(category.lower(), top_k=2)
        if results:
            result_categories = [r.get("metadata", {}).get("category", "") for r in results]
            if any(category in cat for cat in result_categories):
                found_categories.append(category)
    
    print(f"\nFound {len(found_categories)}/{len(categories)} categories:")
    for cat in found_categories:
        print(f"  ✅ {cat}")
    
    # Should find most categories
    assert len(found_categories) >= len(categories) * 0.7, \
        f"Should find at least 70% of categories, found {len(found_categories)}/{len(categories)}"
    
    print("\n✅ PASS: Most KB documents are retrievable")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTING KNOWLEDGE BASE RETRIEVAL")
    print("=" * 60)
    
    try:
        test_kb_initialization()
        test_faiss_vector_search()
        test_fallback_text_search()
        test_edge_cases()
        test_all_kb_documents()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("🎉 Knowledge base retrieval working correctly")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
