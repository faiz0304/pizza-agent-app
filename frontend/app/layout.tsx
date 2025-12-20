'use client';

import type { Metadata } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'
import { CartProvider, useCart } from '@/lib/cart-context'
import FloatingChatWidget from '@/components/FloatingChatWidget'
import { motion } from 'framer-motion'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const poppins = Poppins({
    weight: ['400', '600', '700', '800'],
    subsets: ['latin'],
    variable: '--font-poppins'
})

function NavBar() {
    const { itemCount } = useCart();

    const navLinks = [
        { href: '/', label: 'Home' },
        { href: '/menu', label: 'Menu' },
        { href: '/chat', label: 'Chat' },
        { href: '/order', label: 'Track Order' },
        { href: '/about', label: 'About' },
        { href: '/contact', label: 'Contact' },
    ];

    return (
        <nav className="glass-dark sticky top-0 z-50 border-b border-pizza-orange/30">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <motion.div
                        className="flex items-center"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <h1 className="text-2xl font-bold bg-gradient-to-r from-pizza-red to-pizza-orange bg-clip-text text-transparent">
                            🍕 AGENT-X Pizza
                        </h1>
                    </motion.div>
                    <div className="flex space-x-1">
                        {navLinks.map((link, index) => (
                            <motion.a
                                key={link.href}
                                href={link.href}
                                className="relative px-4 py-2 rounded-lg transition-colors group"
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <span className="relative z-10 group-hover:text-pizza-orange transition-colors duration-200">
                                    {link.label}
                                </span>
                                <motion.div
                                    className="absolute inset-0 bg-pizza-orange/20 rounded-lg"
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    whileHover={{ opacity: 1, scale: 1 }}
                                    transition={{ duration: 0.2 }}
                                />
                                <motion.div
                                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-pizza-red to-pizza-orange"
                                    initial={{ scaleX: 0 }}
                                    whileHover={{ scaleX: 1 }}
                                    transition={{ duration: 0.3 }}
                                />
                            </motion.a>
                        ))}
                        <motion.a
                            href="/cart"
                            className="relative px-4 py-2 rounded-lg transition-colors group"
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.6 }}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <span className="relative z-10 group-hover:text-pizza-orange transition-colors duration-200">
                                Cart
                            </span>
                            {itemCount > 0 && (
                                <motion.span
                                    className="absolute -top-1 -right-1 bg-pizza-red text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center z-20"
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    whileHover={{ scale: 1.2 }}
                                    transition={{ type: 'spring', stiffness: 500 }}
                                >
                                    {itemCount}
                                </motion.span>
                            )}
                            <motion.div
                                className="absolute inset-0 bg-pizza-orange/20 rounded-lg"
                                initial={{ opacity: 0, scale: 0.8 }}
                                whileHover={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.2 }}
                            />
                            <motion.div
                                className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-pizza-red to-pizza-orange"
                                initial={{ scaleX: 0 }}
                                whileHover={{ scaleX: 1 }}
                                transition={{ duration: 0.3 }}
                            />
                        </motion.a>
                    </div>
                </div>
            </div>
        </nav>
    );
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={`${inter.variable} ${poppins.variable} bg-gradient-to-br from-pizza-darker via-pizza-dark to-black min-h-screen text-white`}>
                <CartProvider>
                    <NavBar />
                    <main className="min-h-[calc(100vh-4rem)]">
                        {children}
                    </main>
                    <footer className="glass-dark border-t border-pizza-orange/30 py-8 mt-12">
                        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                            <p className="text-sm text-gray-400">
                                © 2024 AGENT-X Pizza. Powered by AI 🤖 | Built with ❤️ and 🍕
                            </p>
                        </div>
                    </footer>
                    <FloatingChatWidget />
                </CartProvider>
            </body>
        </html>
    )
}
