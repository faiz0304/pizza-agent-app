'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useCart } from '@/lib/cart-context';
import { useRouter } from 'next/navigation';

export default function CheckoutPage() {
    const { items, total, clearCart } = useCart();
    const router = useRouter();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        zipCode: '',
        paymentMethod: 'cash',
        cardNumber: '',
        cardExpiry: '',
        cardCVV: '',
        paypalEmail: ''
    });
    const [orderPlaced, setOrderPlaced] = useState(false);
    const [orderId, setOrderId] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handlePlaceOrder = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            // Prepare order data
            const orderData = {
                user: {
                    name: formData.name,
                    email: formData.email,
                    phone: formData.phone,
                    address: {
                        street: formData.address,
                        city: formData.city,
                        zipCode: formData.zipCode
                    }
                },
                items: items.map(item => ({
                    menu_id: item.id,
                    name: item.name,
                    qty: item.quantity,
                    variant: item.variant,
                    price: item.variantPrice
                })),
                metadata: {
                    payment: {
                        method: formData.paymentMethod,
                        cardLast4: formData.paymentMethod === 'card' ? formData.cardNumber.slice(-4) : undefined,
                        paypalEmail: formData.paymentMethod === 'paypal' ? formData.paypalEmail : undefined
                    },
                    total: parseFloat((total * 1.1).toFixed(2)),
                    subtotal: total,
                    tax: parseFloat((total * 0.1).toFixed(2))
                }
            };

            console.log('Submitting order:', orderData);

            // Use fallback URL if environment variable not set
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            console.log('API URL:', apiUrl);

            // Send to backend
            const response = await fetch(`${apiUrl}/order`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderData)
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Order creation failed:', errorText);
                throw new Error(`Failed to create order: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            console.log('Order created successfully:', result);

            setOrderId(result.order_id || `ORD-${Date.now()}`);
            setOrderPlaced(true);

            // Clear cart after successful order
            setTimeout(() => {
                clearCart();
            }, 2000);
        } catch (error) {
            console.error('Order submission error:', error);
            const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
            alert(`Failed to place order: ${errorMessage}\n\nPlease check the console for details.`);
        } finally {
            setIsSubmitting(false);
        }
    };

    if (items.length === 0 && !orderPlaced) {
        return (
            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="glass-dark rounded-2xl p-12 text-center">
                    <div className="text-6xl mb-4">🛒</div>
                    <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
                    <p className="text-gray-400 mb-6">Add some pizzas before checking out!</p>
                    <a href="/menu">
                        <button className="btn-primary">Browse Menu</button>
                    </a>
                </div>
            </div>
        );
    }

    if (orderPlaced) {
        return (
            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="glass-dark rounded-2xl p-12 text-center"
                >
                    <div className="text-6xl mb-4">🎉</div>
                    <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-pizza-red to-pizza-orange bg-clip-text text-transparent">
                        Order Placed Successfully!
                    </h1>
                    <p className="text-xl text-gray-300 mb-6">
                        Thank you for your order, {formData.name}!
                    </p>
                    <div className="bg-pizza-darker rounded-xl p-6 mb-6">
                        <p className="text-sm text-gray-400 mb-2">Order ID</p>
                        <p className="text-2xl font-bold text-pizza-orange">{orderId}</p>
                    </div>
                    <p className="text-gray-400 mb-8">
                        We've sent a confirmation to <span className="text-white">{formData.email}</span>
                    </p>
                    <div className="flex gap-4 justify-center">
                        <a href="/menu">
                            <button className="bg-pizza-darker border border-pizza-orange/30 hover:bg-pizza-orange/20 px-6 py-3 rounded-xl font-semibold transition-colors">
                                Order More
                            </button>
                        </a>
                        <a href="/order">
                            <button className="btn-primary">
                                Track Order
                            </button>
                        </a>
                    </div>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-pizza-red to-pizza-orange bg-clip-text text-transparent">
                    🛍️ Checkout
                </h1>

                <div className="grid lg:grid-cols-3 gap-8">
                    {/* Checkout Form */}
                    <div className="lg:col-span-2">
                        <form onSubmit={handlePlaceOrder} className="glass-dark rounded-2xl p-6 space-y-6">
                            {/* Contact Information */}
                            <div>
                                <h2 className="text-xl font-bold mb-4">Contact Information</h2>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Full Name *</label>
                                        <input
                                            type="text"
                                            name="name"
                                            required
                                            value={formData.name}
                                            onChange={handleInputChange}
                                            className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                            placeholder="John Doe"
                                        />
                                    </div>
                                    <div className="grid md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium mb-2">Email *</label>
                                            <input
                                                type="email"
                                                name="email"
                                                required
                                                value={formData.email}
                                                onChange={handleInputChange}
                                                className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                                placeholder="john@example.com"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium mb-2">Phone *</label>
                                            <input
                                                type="tel"
                                                name="phone"
                                                required
                                                value={formData.phone}
                                                onChange={handleInputChange}
                                                className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                                placeholder="+1 234 567 8900"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Delivery Address */}
                            <div>
                                <h2 className="text-xl font-bold mb-4">Delivery Address</h2>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-2">Street Address *</label>
                                        <textarea
                                            name="address"
                                            required
                                            value={formData.address}
                                            onChange={handleInputChange}
                                            rows={3}
                                            className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange resize-none"
                                            placeholder="123 Main Street, Apt 4B"
                                        />
                                    </div>
                                    <div className="grid md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium mb-2">City *</label>
                                            <input
                                                type="text"
                                                name="city"
                                                required
                                                value={formData.city}
                                                onChange={handleInputChange}
                                                className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                                placeholder="New York"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium mb-2">ZIP Code *</label>
                                            <input
                                                type="text"
                                                name="zipCode"
                                                required
                                                value={formData.zipCode}
                                                onChange={handleInputChange}
                                                className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                                placeholder="10001"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Payment Method */}
                            <div>
                                <h2 className="text-xl font-bold mb-4">Payment Method</h2>
                                <select
                                    name="paymentMethod"
                                    value={formData.paymentMethod}
                                    onChange={handleInputChange}
                                    className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange mb-4"
                                >
                                    <option value="cash">💵 Cash on Delivery</option>
                                    <option value="card">💳 Credit/Debit Card</option>
                                    <option value="paypal">🅿️ PayPal</option>
                                </select>

                                {/* Conditional Payment Forms */}
                                {formData.paymentMethod === 'card' && (
                                    <div className="space-y-4 mt-4 p-4 bg-pizza-darker rounded-xl border border-pizza-orange/20">
                                        <div>
                                            <label className="block text-sm font-medium mb-2">Card Number *</label>
                                            <input
                                                type="text"
                                                name="cardNumber"
                                                required
                                                maxLength={16}
                                                value={formData.cardNumber}
                                                onChange={handleInputChange}
                                                placeholder="1234 5678 9012 3456"
                                                className="w-full bg-pizza-dark border border-pizza-orange/30 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                            />
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-sm font-medium mb-2">Expiry (MM/YY) *</label>
                                                <input
                                                    type="text"
                                                    name="cardExpiry"
                                                    required
                                                    maxLength={5}
                                                    value={formData.cardExpiry}
                                                    onChange={handleInputChange}
                                                    placeholder="12/25"
                                                    className="w-full bg-pizza-dark border border-pizza-orange/30 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-sm font-medium mb-2">CVV *</label>
                                                <input
                                                    type="text"
                                                    name="cardCVV"
                                                    required
                                                    maxLength={3}
                                                    value={formData.cardCVV}
                                                    onChange={handleInputChange}
                                                    placeholder="123"
                                                    className="w-full bg-pizza-dark border border-pizza-orange/30 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                                />
                                            </div>
                                        </div>
                                        <p className="text-xs text-gray-400 mt-2">🔒 Your card information is secure and encrypted</p>
                                    </div>
                                )}

                                {formData.paymentMethod === 'paypal' && (
                                    <div className="space-y-4 mt-4 p-4 bg-pizza-darker rounded-xl border border-pizza-orange/20">
                                        <div>
                                            <label className="block text-sm font-medium mb-2">PayPal Email *</label>
                                            <input
                                                type="email"
                                                name="paypalEmail"
                                                required
                                                value={formData.paypalEmail}
                                                onChange={handleInputChange}
                                                placeholder="your-paypal@example.com"
                                                className="w-full bg-pizza-dark border border-pizza-orange/30 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                                            />
                                        </div>
                                        <p className="text-xs text-gray-400">You'll be redirected to PayPal to complete payment</p>
                                    </div>
                                )}

                                {formData.paymentMethod === 'cash' && (
                                    <div className="mt-4 p-4 bg-pizza-darker rounded-xl border border-pizza-orange/20">
                                        <p className="text-sm text-gray-400">
                                            💵 Pay with cash when your order is delivered. Please have exact change ready.
                                        </p>
                                    </div>
                                )}
                            </div>

                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="w-full btn-primary text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSubmitting ? 'Processing...' : `Place Order - $${(total * 1.1).toFixed(2)}`}
                            </button>
                        </form>
                    </div>

                    {/* Order Summary */}
                    <div>
                        <div className="glass-dark rounded-2xl p-6 sticky top-24">
                            <h2 className="text-xl font-bold mb-4">Order Summary</h2>

                            <div className="space-y-3 mb-6">
                                {items.map((item) => (
                                    <div key={`${item.id}-${item.variant}`} className="flex justify-between text-sm">
                                        <div className="flex-1">
                                            <p className="font-semibold">{item.name}</p>
                                            <p className="text-gray-400 text-xs capitalize">{item.variant} × {item.quantity}</p>
                                        </div>
                                        <p className="font-semibold text-pizza-orange">
                                            ${(item.variantPrice * item.quantity).toFixed(2)}
                                        </p>
                                    </div>
                                ))}
                            </div>

                            <div className="border-t border-pizza-orange/30 pt-4 space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-400">Subtotal</span>
                                    <span>${total.toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-400">Delivery</span>
                                    <span className="text-green-400">FREE</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-gray-400">Tax (10%)</span>
                                    <span>${(total * 0.1).toFixed(2)}</span>
                                </div>
                                <div className="border-t border-pizza-orange/30 pt-2 flex justify-between text-lg font-bold">
                                    <span>Total</span>
                                    <span className="text-pizza-orange">${(total * 1.1).toFixed(2)}</span>
                                </div>
                            </div>

                            <div className="mt-6 pt-6 border-t border-pizza-orange/30">
                                <div className="flex items-center gap-2 text-sm text-gray-400">
                                    <span>🔒</span>
                                    <span>Secure Checkout</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
