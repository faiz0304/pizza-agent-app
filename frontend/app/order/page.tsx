'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { getOrderStatus } from '@/lib/api-client';

export default function OrderPage() {
    const [orderId, setOrderId] = useState('');
    const [orderData, setOrderData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleTrack = async () => {
        if (!orderId.trim()) return;

        setLoading(true);
        setError('');
        setOrderData(null);

        try {
            const data = await getOrderStatus(orderId);
            setOrderData(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Order not found');
        } finally {
            setLoading(false);
        }
    };

    const statusSteps = ['created', 'confirmed', 'preparing', 'out_for_delivery', 'delivered'];

    const getStatusIndex = (status: string) => {
        const normalized = status.toLowerCase().replace(/\s+/g, '_');
        return statusSteps.indexOf(normalized);
    };

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-pizza-red to-pizza-orange bg-clip-text text-transparent">
                    📦 Track Your Order
                </h1>

                {/* Order ID Input */}
                <div className="glass-dark rounded-2xl p-8 mb-8">
                    <label className="block text-sm font-semibold mb-3">Enter Order ID</label>
                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={orderId}
                            onChange={(e) => setOrderId(e.target.value)}
                            placeholder="ORD-20241204-1234"
                            className="flex-1 bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                            onKeyPress={(e) => e.key === 'Enter' && handleTrack()}
                        />
                        <button
                            onClick={handleTrack}
                            disabled={loading || !orderId.trim()}
                            className="btn-primary px-8"
                        >
                            {loading ? 'Tracking...' : 'Track'}
                        </button>
                    </div>
                    {error && (
                        <p className="text-red-400 mt-3">❌ {error}</p>
                    )}
                </div>

                {/* Order Status Display */}
                {orderData && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="glass-dark rounded-2xl p-8"
                    >
                        {/* Order Info */}
                        <div className="mb-8">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h2 className="text-2xl font-bold mb-2">Order #{orderData.order_id}</h2>
                                    <p className="text-gray-400">
                                        Status: <span className="text-pizza-orange font-semibold">{orderData.status.toUpperCase()}</span>
                                    </p>
                                </div>
                                <div className="text-right">
                                    <div className="text-3xl font-bold text-pizza-orange">${orderData.total}</div>
                                    <div className="text-sm text-gray-500">{orderData.items_count} items</div>
                                </div>
                            </div>
                        </div>

                        {/* Timeline */}
                        <div className="mb-8">
                            <h3 className="text-xl font-bold mb-6">Order Timeline</h3>
                            <div className="relative">
                                {statusSteps.map((step, index) => {
                                    const currentIndex = getStatusIndex(orderData.status);
                                    const isCompleted = index <= currentIndex;
                                    const isCurrent = index === currentIndex;

                                    return (
                                        <div key={step} className="flex items-center mb-8 last:mb-0">
                                            {/* Line */}
                                            {index < statusSteps.length - 1 && (
                                                <div
                                                    className={`absolute left-4 top-12 w-0.5 h-16 ${isCompleted ? 'bg-pizza-orange' : 'bg-gray-700'
                                                        }`}
                                                />
                                            )}

                                            {/* Circle */}
                                            <div
                                                className={`relative z-10 w-8 h-8 rounded-full flex items-center justify-center ${isCompleted
                                                        ? 'bg-pizza-orange glow-orange'
                                                        : 'bg-gray-700'
                                                    }`}
                                            >
                                                {isCompleted && (
                                                    <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                                    </svg>
                                                )}
                                            </div>

                                            {/* Label */}
                                            <div className="ml-4">
                                                <div className={`font-semibold ${isCompleted ? 'text-white' : 'text-gray-500'}`}>
                                                    {step.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                                                </div>
                                                {isCurrent && (
                                                    <div className="text-sm text-pizza-orange">● In Progress</div>
                                                )}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* Tracking Events */}
                        {orderData.tracking && orderData.tracking.length > 0 && (
                            <div>
                                <h3 className="text-xl font-bold mb-4">Tracking History</h3>
                                <div className="space-y-3">
                                    {orderData.tracking.map((event: any, index: number) => (
                                        <div key={index} className="bg-pizza-darker rounded-lg p-4">
                                            <div className="flex justify-between">
                                                <span className="font-semibold capitalize">{event.status.replace('_', ' ')}</span>
                                                <span className="text-sm text-gray-500">
                                                    {new Date(event.timestamp).toLocaleString()}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </motion.div>
                )}

                {/* Sample Order IDs */}
                <div className="mt-8 text-center">
                    <p className="text-sm text-gray-500">
                        Don't have an order ID? Try ordering through our <a href="/chat" className="text-pizza-orange hover:underline">AI assistant</a>!
                    </p>
                </div>
            </motion.div>
        </div>
    );
}
