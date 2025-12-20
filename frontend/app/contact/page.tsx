'use client';

import { motion } from 'framer-motion';

export default function ContactPage() {
    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-16"
            >
                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-pizza-red via-pizza-orange to-pizza-yellow bg-clip-text text-transparent">
                    Get in Touch 📞
                </h1>
                <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                    We're here to help 24/7! Reach out through any of our channels.
                </p>
            </motion.div>

            {/* Contact Methods Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
                {/* Phone */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="glass-dark rounded-2xl p-8 text-center card-hover"
                    whileHover={{ y: -5 }}
                >
                    <div className="text-6xl mb-4">📱</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">Phone</h3>
                    <p className="text-gray-300 mb-2">Customer Service:</p>
                    <a href="tel:1-800-742-9266" className="text-xl font-semibold text-white hover:text-pizza-orange transition-colors">
                        1-800-PIZZA-NOW
                    </a>
                    <p className="text-sm text-gray-400 mt-2">Available 24/7</p>
                </motion.div>

                {/* Email */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="glass-dark rounded-2xl p-8 text-center card-hover"
                    whileHover={{ y: -5 }}
                >
                    <div className="text-6xl mb-4">📧</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">Email</h3>
                    <p className="text-gray-300 mb-2">General Inquiries:</p>
                    <a href="mailto:support@pizzax.com" className="text-xl font-semibold text-white hover:text-pizza-orange transition-colors break-all">
                        support@pizzax.com
                    </a>
                    <p className="text-sm text-gray-400 mt-2">Response within 2 hours</p>
                </motion.div>

                {/* WhatsApp */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="glass-dark rounded-2xl p-8 text-center card-hover"
                    whileHover={{ y: -5 }}
                >
                    <div className="text-6xl mb-4">💬</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">WhatsApp</h3>
                    <p className="text-gray-300 mb-2">Message us:</p>
                    <a href="https://wa.me/14155238886" target="_blank" rel="noopener noreferrer" className="text-xl font-semibold text-white hover:text-pizza-orange transition-colors">
                        +1 (415) 523-8886
                    </a>
                    <p className="text-sm text-gray-400 mt-2">Instant responses</p>
                </motion.div>

                {/* Live Chat */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="glass-dark rounded-2xl p-8 text-center card-hover"
                    whileHover={{ y: -5 }}
                >
                    <div className="text-6xl mb-4">🤖</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">AI Chat</h3>
                    <p className="text-gray-300 mb-2">Chat with AGENT-X:</p>
                    <a href="/chat" className="text-xl font-semibold text-white hover:text-pizza-orange transition-colors">
                        Start Chat
                    </a>
                    <p className="text-sm text-gray-400 mt-2">Always available</p>
                </motion.div>

                {/* Social Media */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="glass-dark rounded-2xl p-8 text-center card-hover"
                    whileHover={{ y: -5 }}
                >
                    <div className="text-6xl mb-4">🌐</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">Social Media</h3>
                    <div className="space-y-2">
                        <a href="https://twitter.com/pizzax" target="_blank" rel="noopener noreferrer" className="block text-white hover:text-pizza-orange transition-colors">
                            Twitter: @PizzaX
                        </a>
                        <a href="https://instagram.com/pizzax" target="_blank" rel="noopener noreferrer" className="block text-white hover:text-pizza-orange transition-colors">
                            Instagram: @PizzaX
                        </a>
                        <a href="https://facebook.com/pizzax" target="_blank" rel="noopener noreferrer" className="block text-white hover:text-pizza-orange transition-colors">
                            Facebook: /PizzaX
                        </a>
                    </div>
                </motion.div>

                {/* Catering */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="glass-dark rounded-2xl p-8 text-center card-hover"
                    whileHover={{ y: -5 }}
                >
                    <div className="text-6xl mb-4">🎉</div>
                    <h3 className="text-2xl font-bold mb-4 text-pizza-orange">Catering</h3>
                    <p className="text-gray-300 mb-2">Events & Parties:</p>
                    <a href="mailto:catering@pizzax.com" className="text-xl font-semibold text-white hover:text-pizza-orange transition-colors break-all">
                        catering@pizzax.com
                    </a>
                    <p className="text-sm text-gray-400 mt-2">48-hour notice preferred</p>
                </motion.div>
            </div>

            {/* Office Hours */}
            <motion.section
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
                className="glass-dark rounded-2xl p-8 mb-12"
            >
                <h2 className="text-3xl font-bold mb-6 text-pizza-orange text-center">Store Hours</h2>
                <div className="grid md:grid-cols-2 gap-6 max-w-2xl mx-auto text-center">
                    <div>
                        <h4 className="font-semibold text-xl mb-2">Monday - Friday</h4>
                        <p className="text-gray-300">10:00 AM - 11:00 PM</p>
                    </div>
                    <div>
                        <h4 className="font-semibold text-xl mb-2">Saturday - Sunday</h4>
                        <p className="text-gray-300">9:00 AM - 12:00 AM</p>
                    </div>
                </div>
                <p className="text-center text-gray-400 mt-6">
                    Closed on Christmas Day and New Year's Day
                </p>
            </motion.section>

            {/* Headquarters */}
            <motion.section
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="glass-dark rounded-2xl p-8 text-center"
            >
                <h2 className="text-3xl font-bold mb-6 text-pizza-orange">Headquarters</h2>
                <div className="text-gray-300 space-y-2">
                    <p className="text-xl">🏢 AGENT-X Pizza HQ</p>
                    <p>123 Pizza Boulevard</p>
                    <p>New York, NY 10001</p>
                    <p>United States</p>
                </div>
            </motion.section>
        </div>
    );
}
