'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';

export default function Home() {
    return (
        <div className="relative overflow-hidden">
            {/* Hero Section */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center"
                >
                    <motion.h1
                        className="text-6xl md:text-8xl font-bold mb-6 bg-gradient-to-r from-pizza-red via-pizza-orange to-pizza-yellow bg-clip-text text-transparent"
                        animate={{ scale: [1, 1.02, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                    >
                        Welcome to <br />
                        AGENT-X Pizza 🍕
                    </motion.h1>

                    <motion.p
                        className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                    >
                        Your AI-powered pizza ordering assistant. Order smarter, not harder.
                    </motion.p>

                    <motion.div
                        className="flex flex-col sm:flex-row gap-4 justify-center"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.6 }}
                    >
                        <Link href="/chat">
                            <motion.button
                                className="btn-primary text-lg px-8 py-4"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                🤖 Chat with Agent
                            </motion.button>
                        </Link>
                        <Link href="/menu">
                            <motion.button
                                className="btn-secondary text-lg px-8 py-4"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                🍕 Browse Menu
                            </motion.button>
                        </Link>
                    </motion.div>
                </motion.div>

                {/* Features Grid */}
                <motion.div
                    className="grid md:grid-cols-3 gap-8 mt-20"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.9 }}
                >
                    <Link href="/chat">
                        <motion.div
                            className="glass-dark p-8 rounded-2xl card-hover cursor-pointer"
                            whileHover={{ y: -10, scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                        >
                            <div className="text-5xl mb-4">🤖</div>
                            <h3 className="text-2xl font-bold mb-3 text-pizza-orange">AI Assistant</h3>
                            <p className="text-gray-400">
                                Chat naturally with AGENT-X. Ask questions, get recommendations, and place orders seamlessly.
                            </p>
                        </motion.div>
                    </Link>

                    <motion.div
                        className="glass-dark p-8 rounded-2xl card-hover"
                        whileHover={{ y: -10 }}
                    >
                        <div className="text-5xl mb-4">⚡</div>
                        <h3 className="text-2xl font-bold mb-3 text-pizza-orange">Fast & Smart</h3>
                        <p className="text-gray-400">
                            Get instant menu searches, personalized recommendations, and real-time order tracking.
                        </p>
                    </motion.div>

                    <motion.div
                        className="glass-dark p-8 rounded-2xl card-hover"
                        whileHover={{ y: -10 }}
                    >
                        <div className="text-5xl mb-4">📱</div>
                        <h3 className="text-2xl font-bold mb-3 text-pizza-orange">Multi-Channel</h3>
                        <p className="text-gray-400">
                            Order from web or WhatsApp. One intelligent agent, multiple ways to connect.
                        </p>
                    </motion.div>
                </motion.div>

                {/* Stats Section */}
                <motion.div
                    className="grid md:grid-cols-4 gap-6 mt-20 text-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.2 }}
                >
                    <div className="glass p-6 rounded-xl">
                        <div className="text-4xl font-bold text-pizza-orange mb-2">10+</div>
                        <div className="text-gray-400">Pizza Varieties</div>
                    </div>
                    <div className="glass p-6 rounded-xl">
                        <div className="text-4xl font-bold text-pizza-orange mb-2">24/7</div>
                        <div className="text-gray-400">AI Support</div>
                    </div>
                    <div className="glass p-6 rounded-xl">
                        <div className="text-4xl font-bold text-pizza-orange mb-2">30min</div>
                        <div className="text-gray-400">Delivery Time</div>
                    </div>
                    <div className="glass p-6 rounded-xl">
                        <div className="text-4xl font-bold text-pizza-orange mb-2">100%</div>
                        <div className="text-gray-400">Fresh Ingredients</div>
                    </div>
                </motion.div>
            </div>

            {/* Background Elements */}
            <div className="absolute top-20 right-20 w-72 h-72 bg-pizza-red/10 rounded-full blur-3xl animate-pulse-slow"></div>
            <div className="absolute bottom-20 left-20 w-96 h-96 bg-pizza-orange/10 rounded-full blur-3xl animate-pulse-slow"></div>
        </div>
    );
}
