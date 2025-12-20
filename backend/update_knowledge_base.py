"""
Knowledge Base Content Expansion
Run this script to populate the knowledge base with comprehensive Q&A
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rag_tool import rag_tool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_comprehensive_knowledge():
    """Add comprehensive knowledge base content for all query categories"""
    
    # Comprehensive knowledge base documents
    kb_documents = [
        # ===== MENU & PRODUCT INFORMATION =====
        "Our pizza menu includes 15+ varieties: Margherita ($10.99), Pepperoni Classic ($12.99), Hawaiian ($11.99), BBQ Chicken ($13.99), Vegetarian Special ($11.99), Meat Lovers ($14.99), Supreme ($13.99), Four Cheese ($12.99), Buffalo Chicken ($13.99), Mexican ($12.99), Mediterranean ($13.99), Pesto Veggie ($12.99), Philly Cheesesteak ($14.99), and specialty seasonal pizzas.",
        
        "Vegetarian options: Margherita (tomato, mozzarella, basil), Vegetarian Special (bell peppers, onions, mushrooms, olives, tomatoes), Four Cheese (mozzarella, cheddar, parmesan, goat cheese), Pesto Veggie (basil pesto, spinach, artichokes, sun-dried tomatoes), and Mediterranean (feta, olives, spinach, red onion).",
        
        "Vegan options available! We offer vegan cheese ($2 extra) and can make any veggie pizza vegan. Try our Vegan Mediterranean or build your own. Gluten-free crust available for all pizzas ($3 extra), made in a separate area to avoid cross-contamination.",
        
        "Pizza sizes: Small (10 inch, 6 slices, $8-$10), Medium (12 inch, 8 slices, $10-$13), Large (14 inch, 10 slices, $13-$16), Extra Large (16 inch, 12 slices, $16-$19). Prices vary by toppings.",
        
        "Available toppings: Veggies (bell peppers, onions, mushrooms, olives, tomatoes, spinach, jalapeños, pineapple), Meats (pepperoni, sausage, ham, bacon, chicken, beef), Premium (feta, goat cheese, sun-dried tomatoes, artichokes, anchovies). Extra toppings: $1.50 regular, $2 premium.",
        
        "Combo deals: 2 Large Pizzas + Garlic Bread + 2L Soda ($35), Family Pack (3 Medium Pizzas + Wings + Dessert $45), Student Meal (1 Medium + Drink $12), Party Pack (5 Large Pizzas + 3 Sides $75). Deals change weekly!",
        
        "Customize your pizza: Choose crust (regular, thin, thick, stuffed, gluten-free), sauce (tomato, white, BBQ, pesto, ranch), cheese level (light, regular, extra), and add unlimited toppings. Build exactly what you want!",
        
        "Drinks: Coca-Cola, Pepsi, Sprite, Fanta, Diet Coke (600ml $2, 2L $5), Fresh Juices (Orange, Apple, Mango $3), Iced Tea ($2.50), Water ($1). Sides: Garlic Bread ($4), Chicken Wings (6pc $7, 12pc $12), Mozzarella Sticks ($6), Caesar Salad ($5), French Fries ($4), Dessert Pizza ($8).",
        
        # ===== ORDERING & CART =====
        "Place orders 3 ways: 1) Website - Browse menu, add to cart, checkout. 2) WhatsApp - Message us your order at +1-415-523-8886. 3) Phone - Call 1-800-PIZZA-NOW. 4) Mobile App - Download from App Store/Play Store.",
        
        "How to order: Browse menu → Select pizza → Choose size → Add toppings → Add to cart → Review cart → Enter delivery address → Choose payment → Confirm order. You'll get an order ID immediately!",
        
        "Cart management: Add items anytime, update quantities with +/- buttons, remove items with X button. Cart saves automatically. View cart total before checkout. Apply promo codes at checkout.",
        
        "Save cart for later? Yes! Your cart persists across sessions. Come back anytime to complete your order. Cart expires after 7 days of inactivity.",
        
        "Promo codes: Apply at checkout. Enter code in 'Promo Code' field → Click Apply. Discount shows in order summary. One code per order. Cannot combine codes. Check app for active codes!",
        
        # ===== DELIVERY & PICKUP =====
        "Delivery areas: We deliver within 10km radius of each store. Enter your address at checkout to check availability. Free delivery on orders $25+, otherwise $3 delivery fee.",
        
        "Delivery time: Average 25-35 minutes. During peak hours (6-9 PM) may take up to 45 minutes. You'll get real-time tracking with estimated arrival time. We guarantee hot, fresh pizza!",
        
        "Schedule delivery: Yes! Order up to 24 hours in advance. Choose 'Schedule for Later' at checkout, select date and time. Minimum 2 hours notice required. Perfect for parties!",
        
        "Pickup option: Save on delivery! Order online, choose 'Pickup', select store and time. Get 10% off pickup orders. Show order ID at counter. Average ready time: 15-20 minutes.",
        
        "Nearest store: Use our store locator on website or app. Enter zip code or allow location access. Shows all stores with addresses, phone numbers, and hours. Choose closest for fastest delivery!",
        
        "Contactless delivery: Standard for all orders! Driver leaves pizza at door, rings bell/knocks, steps back. Payment is prepaid online. Instructions in app for safe delivery.",
        
        # ===== PAYMENT & OFFERS =====
        "Payment methods: Credit/Debit Cards (Visa, Mastercard, Amex), Cash on Delivery, Digital Wallets (PayPal, Google Pay, Apple Pay, Venmo), Cryptocurrency (Bitcoin, Ethereum via Coinbase). All payments secure with SSL encryption.",
        
        "Cash on Delivery: Available! Select 'Cash' at checkout. Have exact change ready. Driver carries max $20 change. COD available for orders under $100.",
        
        "Online wallets: Pay with PayPal, Google Pay, Apple Pay for fastest checkout. Save payment method for one-click ordering. UPI accepted for Indian customers.",
        
        "Ongoing offers: 🎉 Buy 2 Large, Get 1 Medium Free! 🎓 Student Discount 15% off (valid ID required). 🎁 First Order 10% off (code: FIRST10). 🍕 Weekend Special: 20% off orders over $40 (Sat-Sun). 💰 Loyalty points: Earn $1 = 1 point. Check app daily!",
        
        "Multiple promo codes: Sorry, one code per order. System automatically applies best discount. Choose the code that saves you most!",
        
        # ===== ORDER TRACKING & HISTORY =====
        "Track your order: Use order ID sent via email/SMS. Visit Track Order page → Enter order ID → See real-time status: Created → Confirmed → Preparing → Baking → Out for Delivery → Delivered. Average updates every 3-5 minutes.",
        
        "Order status meanings: Created (order received), Confirmed (payment verified), Preparing (gathering ingredients), Baking (in oven), Quality Check (ensuring perfection), Out for Delivery (on the way!), Delivered (enjoy!).",
        
        "Estimated arrival: Based on current prep time + delivery distance. Updates in real-time. If delayed, you'll get SMS notification with new ETA. Late orders get automatic 10% refund.",
        
        "Order history: Login to account → My Orders → See all past orders with dates, items, totals. Reorder with one click! Download receipts as PDF. Track spending and loyalty points.",
        
        "Repeat order: Find order in history → Click 'Reorder' → Items added to cart → Modify if needed → Checkout. Saves time for favorites!",
        
        # ===== ACCOUNT & PROFILE =====
        "Create account: Click 'Sign Up' → Enter name, email, password, phone → Verify email → Account ready! Benefits: faster checkout, order history, loyalty points, saved addresses, exclusive offers.",
        
        "Login: Click 'Login' → Enter email/phone + password → Access account. Or use Google/Facebook login for quick access.",
        
        "Forgot password: Click 'Forgot Password' → Enter email → Check inbox for reset link → Create new password → Login with new password. Reset link valid 1 hour.",
        
        "Update profile: Login → Account Settings → Edit name, email, phone, password. Add profile picture. Set delivery preferences. Manage saved addresses. Update notification preferences.",
        
        "Add delivery address: Account → Addresses → Add New → Enter street, city, zip, landmark → Save. Add multiple addresses (home, work, etc.). Set default address for quick checkout.",
        
        # ===== SUPPORT & FEEDBACK =====
        "Order problems: Wrong items, missing items, cold pizza, damaged box? Contact support immediately! Call 1-800-PIZZA-NOW, email support@pizzax.com, or use live chat. We'll replace or refund within 2 hours!",
        
        "Cancel order: Cancellation free within 5 minutes of placing order. After that: $3 cancellation fee if not yet preparing. Cannot cancel once 'Baking' status. Full refund if eligible.",
        
        "Report issues: Wrong order? Go to Order Details → Report Problem → Select issue (wrong items, missing items, quality issue, late delivery) → Upload photo if helpful → Submit. Support responds in 15 minutes!",
        
        "Contact support: Phone: 1-800-PIZZA-NOW (24/7), Email: support@pizzax.com (response in 2 hours), Live Chat: website/app (instant), WhatsApp: +1-415-523-8886, Social: @PizzaX on Twitter/Instagram.",
        
        "Provide feedback: After delivery → Rate order 1-5 stars → Leave comment (optional) → Submit. Earn 10 loyalty points for feedback! Help us improve!",
        
        "Service rating: Rate delivery speed, food quality, packaging, driver courtesy. Your feedback helps us serve you better. Top-rated drivers get bonuses!",
        
        # ===== MISCELLANEOUS =====
        "Store hours: Monday-Friday: 10 AM - 11 PM, Saturday-Sunday: 9 AM - 12 AM (midnight). Delivery until 30 min before closing. Closed Christmas Day, New Year's Day. Extended hours during Super Bowl!",
        
        "Catering services: Yes! Order for parties, events, corporate meetings. Minimum order: 10 Large Pizzas. Get: free delivery, bulk discounts (15-20% off), dedicated support, customized packaging. Call 1-800-CATER-PIZZA or email catering@pizzax.com. 48-hour advance notice preferred.",
        
        "Loyalty program: Pizza Rewards! Earn 1 point per $1 spent. Redeem: 100 points = $10 off, 250 points = Free Medium Pizza, 500 points = Free Large + Drink. Birthday reward: Free Dessert Pizza! No expiration. Join free in app!",
        
        "Gift cards: Available in $10, $25, $50, $100 denominations. Buy online or in-store. Send digital gift cards via email instantly. Perfect gifts! Valid 1 year. No fees!",
        
        "Seasonal pizzas: Limited-time specials! Current: Pumpkin Spice Pizza (Oct), Truffle Mushroom (Nov), Candy Cane Dessert Pizza (Dec), Heart-Shaped Valentine's (Feb). Check app for current seasonal pizzas! Available 4-6 weeks only.",
        
        "Allergen info: All pizzas contain gluten (wheat) and dairy unless specified. Vegan and gluten-free options available. Nuts in: Pesto Veggie. Eggs in: Some dressings. Soy in: Some meat substitutes. Inform us of allergies - we have protocols!",
        
        "Nutritional information: Average Medium Pizza (12 inch): 1200-1500 calories, 40-60g protein, 150-200g carbs, 40-70g fat. Veggie pizzas lower in calories. Full nutrition guide at pizzax.com/nutrition. Request allergen chart at order!",
        
        "Company story: Founded 1995 in New York. Started with 1 oven, now 500+ locations nationwide! Family-owned, committed to quality. Fresh ingredients, community-focused. Won 'Best Pizza' award 10 years running!",
        
        "Sustainability: We care! Recyclable packaging, electric delivery vehicles (50% of fleet), local sourcing, composting food waste, solar panels on stores. Carbon-neutral by 2025!",
    ]
    
    # Metadata for each document
    kb_metadatas = [
        # Menu & Product (9 entries)
        {"category": "Menu", "title": "Pizza Menu Overview", "source": "product_catalog"},
        {"category": "Menu", "title": "Vegetarian Options", "source": "product_catalog"},
        {"category": "Menu", "title": "Vegan & Gluten-Free", "source": "product_catalog"},
        {"category": "Menu", "title": "Pizza Sizes", "source": "product_catalog"},
        {"category": "Menu", "title": "Available Toppings", "source": "product_catalog"},
        {"category": "Menu", "title": "Combo Deals", "source": "marketing"},
        {"category": "Menu", "title": "Pizza Customization", "source": "product_info"},
        {"category": "Menu", "title": "Drinks and Sides", "source": "product_catalog"},
        
        # Ordering & Cart (5 entries)
        {"category": "Ordering", "title": "How to Place Order", "source": "user_guide"},
        {"category": "Ordering", "title": "Ordering Process", "source": "user_guide"},
        {"category": "Ordering", "title": "Cart Management", "source": "user_guide"},
        {"category": "Ordering", "title": "Save Cart Feature", "source": "user_guide"},
        {"category": "Ordering", "title": "Promo Codes", "source": "marketing"},
        
        # Delivery & Pickup (6 entries)
        {"category": "Delivery", "title": "Delivery Areas", "source": "company_policy"},
        {"category": "Delivery", "title": "Delivery Time", "source": "company_policy"},
        {"category": "Delivery", "title": "Schedule Delivery", "source": "user_guide"},
        {"category": "Delivery", "title": "Pickup Option", "source": "user_guide"},
        {"category": "Delivery", "title": "Store Locator", "source": "company_info"},
        {"category": "Delivery", "title": "Contactless Delivery", "source": "company_policy"},
        
        # Payment & Offers (5 entries)
        {"category": "Payment", "title": "Payment Methods", "source": "company_policy"},
        {"category": "Payment", "title": "Cash on Delivery", "source": "company_policy"},
        {"category": "Payment", "title": "Online Wallets", "source": "company_policy"},
        {"category": "Offers", "title": "Current Offers", "source": "marketing"},
        {"category": "Offers", "title": "Multiple Promo Codes", "source": "marketing"},
        
        # Order Tracking (5 entries)
        {"category": "Tracking", "title": "How to Track Order", "source": "user_guide"},
        {"category": "Tracking", "title": "Order Status Meanings", "source": "user_guide"},
        {"category": "Tracking", "title": "Estimated Arrival", "source": "user_guide"},
        {"category": "Tracking", "title": "Order History", "source": "user_guide"},
        {"category": "Tracking", "title": "Repeat Order", "source": "user_guide"},
        
        # Account & Profile (5 entries)
        {"category": "Account", "title": "Create Account", "source": "user_guide"},
        {"category": "Account", "title": "Login", "source": "user_guide"},
        {"category": "Account", "title": "Forgot Password", "source": "user_guide"},
        {"category": "Account", "title": "Update Profile", "source": "user_guide"},
        {"category": "Account", "title": "Add Delivery Address", "source": "user_guide"},
        
        # Support & Feedback (6 entries)
        {"category": "Support", "title": "Order Problems", "source": "company_policy"},
        {"category": "Support", "title": "Cancel Order", "source": "company_policy"},
        {"category": "Support", "title": "Report Issues", "source": "user_guide"},
        {"category": "Support", "title": "Contact Support", "source": "company_info"},
        {"category": "Support", "title": "Provide Feedback", "source": "user_guide"},
        {"category": "Support", "title": "Service Rating", "source": "user_guide"},
        
        # Miscellaneous (9 entries)
        {"category": "Miscellaneous", "title": "Store Hours", "source": "company_info"},
        {"category": "Miscellaneous", "title": "Catering Services", "source": "company_info"},
        {"category": "Miscellaneous", "title": "Loyalty Program", "source": "marketing"},
        {"category": "Miscellaneous", "title": "Gift Cards", "source": "marketing"},
        {"category": "Miscellaneous", "title": "Seasonal Pizzas", "source": "product_catalog"},
        {"category": "Miscellaneous", "title": "Allergen Information", "source": "product_info"},
        {"category": "Miscellaneous", "title": "Nutritional Information", "source": "product_info"},
        {"category": "Miscellaneous", "title": "Company Story", "source": "company_info"},
        {"category": "Miscellaneous", "title": "Sustainability", "source": "company_info"},
    ]
    
    # Generate IDs
    start_id = rag_tool.collection.count() + 1
    kb_ids = [f"kb_{i+start_id:03d}" for i in range(len(kb_documents))]
    
    # Add to vector store
    logger.info(f"Adding {len(kb_documents)} new knowledge base documents...")
    rag_tool.add_documents(kb_documents, kb_metadatas, kb_ids)
    
    logger.info(f"✅ Knowledge base updated! Total documents: {rag_tool.collection.count()}")
    logger.info("Categories covered: Menu, Ordering, Delivery, Payment, Offers, Tracking, Account, Support, Miscellaneous")


if __name__ == "__main__":
    add_comprehensive_knowledge()
    print("\n✅ Knowledge base successfully updated with comprehensive content!")
    print("🎯 The chatbot can now answer 50+ different query types across all channels!")
