#!/bin/bash
# Automated Test Runner for Agentic Pizza Ordering System
# Run all backend, frontend, and integration tests

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🍕 Agentic Pizza Testing Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to run test and track results
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}Testing: ${test_name}${NC}"
    
    if eval $test_command > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check if servers are running
echo -e "${BLUE}📡 Checking Server Status...${NC}"
echo ""

# Backend health check
run_test "Backend Health" "curl -s http://localhost:8000/health | grep -q '\"status\":\"healthy\"'"

# Frontend check
run_test "Frontend Accessible" "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000 | grep -q 200"

echo ""
echo -e "${BLUE}🔧 Backend API Tests...${NC}"
echo ""

# Menu tests
run_test "Menu Listing" "curl -s http://localhost:8000/menu | grep -q '\"items\"'"
run_test "Menu Search" "curl -s 'http://localhost:8000/menu/search?q=pizza' | grep -q '\"items\"'"

# Chatbot tests
run_test "Chatbot Simple Greeting" "curl -s -X POST http://localhost:8000/chatbot -H 'Content-Type: application/json' -d '{\"message\":\"Hello\",\"user_id\":\"test\"}' | grep -q '\"reply\"'"
run_test "Chatbot Menu Search" "curl -s -X POST http://localhost:8000/chatbot -H 'Content-Type: application/json' -d '{\"message\":\"Show me pizzas\",\"user_id\":\"test\"}' | grep -q '\"reply\"'"
run_test "Chatbot KB Search" "curl -s -X POST http://localhost:8000/chatbot -H 'Content-Type: application/json' -d '{\"message\":\"refund policy\",\"user_id\":\"test\"}' | grep -q '\"reply\"'"

echo ""
echo -e "${BLUE}🌐 Frontend Tests...${NC}"
echo ""

# Frontend page tests
run_test "Landing Page" "curl -s http://localhost:3000 | grep -q 'AGENT-X Pizza'"
run_test "Chat Page" "curl -s http://localhost:3000/chat | grep -q 'Chat with AGENT-X'"
run_test "Menu Page" "curl -s http://localhost:3000/menu | grep -q 'Our Menu'"
run_test "Cart Page" "curl -s http://localhost:3000/cart | grep -q 'Shopping Cart'"
run_test "Order Page" "curl -s http://localhost:3000/order | grep -q 'Track Your Order'"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📊 Test Results Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✅ Passed: ${TESTS_PASSED}${NC}"
echo -e "${RED}❌ Failed: ${TESTS_FAILED}${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Check the output above.${NC}"
    exit 1
fi
