"""
Automated Test Runner for Agentic Pizza Ordering System
Runs all backend, frontend, and integration tests
"""
import requests
import sys
import time
from colorama import Fore, Style, init

# Initialize colorama for Windows
init()

class TestRunner:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def print_header(self, text):
        print(f"\n{Fore.BLUE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{text}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}\n")
    
    def run_test(self, name, test_func):
        """Run a single test and track results"""
        print(f"{Fore.YELLOW}Testing: {name}{Style.RESET_ALL}", end=" ... ")
        
        try:
            result = test_func()
            if result:
                print(f"{Fore.GREEN}✅ PASS{Style.RESET_ALL}")
                self.tests_passed += 1
                self.results.append((name, True, None))
            else:
                print(f"{Fore.RED}❌ FAIL{Style.RESET_ALL}")
                self.tests_failed += 1
                self.results.append((name, False, "Test returned False"))
        except Exception as e:
            print(f"{Fore.RED}❌ FAIL - {str(e)}{Style.RESET_ALL}")
            self.tests_failed += 1
            self.results.append((name, False, str(e)))
    
    # Server status tests
    def test_backend_health(self):
        response = requests.get(f"{self.backend_url}/health", timeout=5)
        return response.status_code == 200 and response.json().get("status") == "healthy"
    
    def test_frontend_accessible(self):
        response = requests.get(self.frontend_url, timeout=5)
        return response.status_code == 200
    
    # Backend API tests
    def test_menu_listing(self):
        response = requests.get(f"{self.backend_url}/menu", timeout=5)
        data = response.json()
        return "items" in data and len(data["items"]) > 0
    
    def test_menu_search(self):
        response = requests.get(f"{self.backend_url}/menu/search?q=pizza", timeout=5)
        data = response.json()
        return "items" in data
    
    def test_chatbot_greeting(self):
        payload = {"message": "Hello", "user_id": "test_user"}
        response = requests.post(f"{self.backend_url}/chatbot", json=payload, timeout=10)
        data = response.json()
        return "reply" in data and data["status"] == "success"
    
    def test_chatbot_menu_search(self):
        payload = {"message": "Show me pizzas", "user_id": "test_user"}
        response = requests.post(f"{self.backend_url}/chatbot", json=payload, timeout=15)
        data = response.json()
        return "reply" in data and data["status"] == "success"
    
    def test_chatbot_kb_search(self):
        payload = {"message": "What is your refund policy?", "user_id": "test_user"}
        response = requests.post(f"{self.backend_url}/chatbot", json=payload, timeout=15)
        data = response.json()
        return "reply" in data and data["status"] == "success"
    
    # Frontend page tests
    def test_landing_page(self):
        response = requests.get(self.frontend_url, timeout=5)
        return "AGENT-X" in response.text
    
    def test_chat_page(self):
        response = requests.get(f"{self.frontend_url}/chat", timeout=15)
        return "Chat with AGENT-X" in response.text or "chat" in response.text.lower()
    
    def test_menu_page(self):
        response = requests.get(f"{self.frontend_url}/menu", timeout=15)
        return "menu" in response.text.lower()
    
    def test_cart_page(self):
        response = requests.get(f"{self.frontend_url}/cart", timeout=5)
        return "cart" in response.text.lower()
    
    def test_order_page(self):
        response = requests.get(f"{self.frontend_url}/order", timeout=5)
        return "order" in response.text.lower() or "track" in response.text.lower()
    
    def run_all_tests(self):
        """Run all test suites"""
        print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}🍕 Agentic Pizza Testing Suite{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*50}{Style.RESET_ALL}")
        
        # Server status
        self.print_header("📡 Server Status Tests")
        self.run_test("Backend Health", self.test_backend_health)
        self.run_test("Frontend Accessible", self.test_frontend_accessible)
        
        # Backend tests
        self.print_header("🔧 Backend API Tests")
        self.run_test("Menu Listing", self.test_menu_listing)
        self.run_test("Menu Search", self.test_menu_search)
        self.run_test("Chatbot Greeting", self.test_chatbot_greeting)
        self.run_test("Chatbot Menu Search", self.test_chatbot_menu_search)
        self.run_test("Chatbot KB Search", self.test_chatbot_kb_search)
        
        # Frontend tests
        self.print_header("🌐 Frontend Page Tests")
        self.run_test("Landing Page", self.test_landing_page)
        self.run_test("Chat Page", self.test_chat_page)
        self.run_test("Menu Page", self.test_menu_page)
        self.run_test("Cart Page", self.test_cart_page)
        self.run_test("Order Page", self.test_order_page)
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        self.print_header("📊 Test Results Summary")
        
        print(f"{Fore.GREEN}✅ Passed: {self.tests_passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}❌ Failed: {self.tests_failed}{Style.RESET_ALL}")
        print()
        
        if self.tests_failed > 0:
            print(f"{Fore.RED}Failed Tests:{Style.RESET_ALL}")
            for name, passed, error in self.results:
                if not passed:
                    print(f"  - {name}: {error}")
            print()
        
        if self.tests_failed == 0:
            print(f"{Fore.GREEN}🎉 All tests passed!{Style.RESET_ALL}")
            return 0
        else:
            print(f"{Fore.RED}⚠️  {self.tests_failed} test(s) failed.{Style.RESET_ALL}")
            return 1


if __name__ == "__main__":
    runner = TestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)
