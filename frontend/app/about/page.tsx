'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';

export default function AboutPage() {
    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-16"
            >
                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-pizza-red via-pizza-orange to-pizza-yellow bg-clip-text text-transparent">
                    About AGENT-X Pizza 🍕
                </h1>
                <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                    Where AI meets artisanal pizza craftsmanship
                </p>
            </motion.div>

            {/* Story Section */}
            <motion.section
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="glass-dark rounded-2xl p-8 md:p-12 mb-12"
            >
                <h2 className="text-3xl font-bold mb-6 text-pizza-orange">Our Story</h2>
                <div className="space-y-4 text-gray-300 leading-relaxed">
                    <p>
                        Founded in 1995 in the heart of New York City, AGENT-X Pizza started with a simple vision:
                        combine traditional Italian pizza-making with cutting-edge technology to create the ultimate ordering experience.
                    </p>
                    <p>
                        What began as a single oven in a small storefront has grown into 500+ locations nationwide.
                        But we've never forgotten our roots – every pizza is still crafted with the same care and
                        quality ingredients that made us famous.
                    </p>
                    <p>
                        In 2020, we revolutionized pizza ordering by introducing AGENT-X, our AI-powered assistant
                        that makes ordering faster, smarter, and more personalized than ever before.
                    </p>
                </div>
            </motion.section>

            {/* Mission & Values */}
            <div className="grid md:grid-cols-2 gap-8 mb-12">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 }}
                    className="glass-dark rounded-2xl p-8"
                >
                    <div className="text-5xl mb-4">🎯</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">Our Mission</h3>
                    <p className="text-gray-300">
                        To deliver hot, delicious, high-quality pizzas using fresh ingredients and
                        innovative technology – making every customer's experience exceptional.
                    </p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                    className="glass-dark rounded-2xl p-8"
                >
                    <div className="text-5xl mb-4">💎</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">Our Values</h3>
                    <ul className="text-gray-300 space-y-2">
                        <li>✅ Quality ingredients, no compromises</li>
                        <li>✅ Innovation in every slice</li>
                        <li>✅ Community-focused and family-owned</li>
                        <li>✅ Sustainable and eco-friendly</li>
                    </ul>
                </motion.div>
            </div>

            {/* What Makes Us Special */}
            <motion.section
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="glass-dark rounded-2xl p-8 md:p-12 mb-12"
            >
                <h2 className="text-3xl font-bold mb-8 text-pizza-orange text-center">What Makes Us Special</h2>
                <div className="grid md:grid-cols-3 gap-6">
                    <div className="text-center">
                        <div className="text-5xl mb-4">🌱</div>
                        <h4 className="text-xl font-semibold mb-3">Fresh Ingredients</h4>
                        <p className="text-gray-400 text-sm">
                            100% fresh, locally-sourced ingredients. Dough made fresh daily with organic flour.
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="text-5xl mb-4">🤖</div>
                        <h4 className="text-xl font-semibold mb-3">AI-Powered Service</h4>
                        <p className="text-gray-400 text-sm">
                            24/7 intelligent assistant for instant ordering, tracking, and customer support.
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="text-5xl mb-4">🌍</div>
                        <h4 className="text-xl font-semibold mb-3">Eco-Friendly</h4>
                        <p className="text-gray-400 text-sm">
                            Recyclable packaging, electric delivery vehicles, solar-powered stores. Carbon-neutral by 2025.
                        </p>
                    </div>
                </div>
            </motion.section>

            {/* Awards & Recognition */}
            <motion.section
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="glass-dark rounded-2xl p-8 text-center mb-12"
            >
                <h2 className="text-3xl font-bold mb-6 text-pizza-orange">Awards & Recognition</h2>
                <div className="flex flex-wrap justify-center gap-6 text-gray-300">
                    <div>🏆 Best Pizza Award (10 years running)</div>
                    <div>⭐ 4.9/5 Customer Rating</div>
                    <div>🥇 Innovation in Food Tech 2023</div>
                    <div>🌟 Top 100 Restaurants Nationwide</div>
                </div>
            </motion.section>

            {/* CTA */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
                className="text-center"
            >
                <Link href="/menu">
                    <motion.button
                        className="btn-primary text-lg px-10 py-4"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        Order Now 🍕
                    </motion.button>
                </Link>
            </motion.div>
        </div>
    );
}
