'use client';

import { useCart } from '@/lib/cart-context';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';

export default function CartPage() {
    const { items, removeFromCart, updateQuantity, total, clearCart } = useCart();
    const router = useRouter();

    const handleCheckout = () => {
        if (items.length > 0) {
            router.push('/checkout');
        }
    };

    return (
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold bg-gradient-to-r from-pizza-red to-pizza-orange bg-clip-text text-transparent">
                        🛒 Shopping Cart
                    </h1>
                    {items.length > 0 && (
                        <button onClick={clearCart} className="text-sm text-gray-400 hover:text-pizza-red transition-colors">
                            Clear Cart
                        </button>
                    )}
                </div>

                {items.length === 0 ? (
                    <div className="glass-dark rounded-2xl p-12 text-center">
                        <div className="text-6xl mb-4">🛒</div>
                        <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
                        <p className="text-gray-400 mb-6">Add some delicious pizzas to get started!</p>
                        <a href="/menu">
                            <button className="btn-primary">
                                Browse Menu
                            </button>
                        </a>
                    </div>
                ) : (
                    <div className="grid lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 space-y-4">
                            {items.map((item) => (
                                <motion.div
                                    key={`${item.id}-${item.variant}`}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    className="glass-dark rounded-xl p-6 flex gap-6"
                                >
                                    <div className="flex-shrink-0 w-24 h-24 bg-gradient-to-br from-pizza-orange/20 to-pizza-red/20 rounded-xl flex items-center justify-center">
                                        <div className="text-5xl">🍕</div>
                                    </div>

                                    <div className="flex-grow">
                                        <div className="flex justify-between mb-2">
                                            <div>
                                                <h3 className="text-xl font-bold">{item.name}</h3>
                                                <p className="text-sm text-gray-400 capitalize">{item.variant} Size</p>
                                            </div>
                                            <button
                                                onClick={() => removeFromCart(item.id, item.variant)}
                                                className="text-pizza-red hover:text-pizza-orange transition-colors"
                                            >
                                                ✕
                                            </button>
                                        </div>

                                        <div className="flex items-center justify-between mt-4">
                                            <div className="flex items-center gap-3">
                                                <button
                                                    onClick={() => updateQuantity(item.id, item.quantity - 1, item.variant)}
                                                    className="w-8 h-8 rounded-lg bg-pizza-darker border border-pizza-orange/30 hover:bg-pizza-orange/20 transition-colors"
                                                >
                                                    −
                                                </button>
                                                <span className="text-lg font-semibold w-8 text-center">{item.quantity}</span>
                                                <button
                                                    onClick={() => updateQuantity(item.id, item.quantity + 1, item.variant)}
                                                    className="w-8 h-8 rounded-lg bg-pizza-darker border border-pizza-orange/30 hover:bg-pizza-orange/20 transition-colors"
                                                >
                                                    +
                                                </button>
                                            </div>

                                            <div className="text-right">
                                                <div className="text-xl font-bold text-pizza-orange">
                                                    ${(item.variantPrice * item.quantity).toFixed(2)}
                                                </div>
                                                <div className="text-xs text-gray-500">
                                                    ${item.variantPrice.toFixed(2)} each
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </div>

                        <div className="glass-dark rounded-2xl p-6 h-fit sticky top-24">
                            <h3 className="text-xl font-bold mb-4">Order Summary</h3>
                            <div className="space-y-3 mb-6">
                                <div className="flex justify-between">
                                    <span className="text-gray-400">Items ({items.reduce((sum, item) => sum + item.quantity, 0)})</span>
                                    <span className="font-semibold">${total.toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-gray-400">Delivery</span>
                                    <span className="font-semibold text-green-400">FREE</span>
                                </div>
                                <div className="border-t border-pizza-orange/30 pt-3 flex justify-between text-lg">
                                    <span className="font-bold">Total</span>
                                    <span className="font-bold text-pizza-orange">${total.toFixed(2)}</span>
                                </div>
                            </div>
                            <button
                                onClick={handleCheckout}
                                disabled={items.length === 0}
                                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Proceed to Checkout
                            </button>
                            <a href="/menu">
                                <button className="w-full bg-pizza-darker border border-pizza-orange/30 hover:bg-pizza-orange/20 py-3 rounded-xl font-semibold transition-colors">
                                    Continue Shopping
                                </button>
                            </a>
                        </div>
                    </div>
                )}
            </motion.div>
        </div>
    );
}
