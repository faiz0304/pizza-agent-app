'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getMenu, searchMenu, type MenuItem } from '@/lib/api-client';
import { useCart } from '@/lib/cart-context';

export default function MenuPage() {
    const { addToCart } = useCart();
    const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
    const [filteredItems, setFilteredItems] = useState<MenuItem[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [isLoading, setIsLoading] = useState(true);
    const [showToast, setShowToast] = useState(false);
    const [toastMessage, setToastMessage] = useState('');

    useEffect(() => {
        loadMenu();
    }, []);

    const loadMenu = async () => {
        try {
            setIsLoading(true);
            const items = await getMenu();
            setMenuItems(items);
            setFilteredItems(items);
        } catch (error) {
            console.error('Error loading menu:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSearch = async (query: string) => {
        setSearchQuery(query);
        if (!query.trim()) {
            setFilteredItems(menuItems);
            return;
        }

        try {
            const results = await searchMenu(query);
            setFilteredItems(results);
        } catch (error) {
            console.error('Search error:', error);
        }
    };

    const filterByCategory = (category: string) => {
        setSelectedCategory(category);
        setSearchQuery('');

        if (category === 'all') {
            setFilteredItems(menuItems);
        } else {
            setFilteredItems(menuItems.filter(item =>
                item.category.toLowerCase() === category.toLowerCase()
            ));
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-pizza-red to-pizza-orange bg-clip-text text-transparent">
                        🍕 Our Menu
                    </h1>
                    <p className="text-xl text-gray-400">
                        Fresh, delicious pizzas made with love
                    </p>
                </div>

                {/* Search Bar */}
                <div className="mb-8">
                    <div className="max-w-2xl mx-auto">
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => handleSearch(e.target.value)}
                            placeholder="Search pizzas by name, ingredients, or tags..."
                            className="w-full bg-pizza-darker border border-pizza-orange/30 rounded-xl px-6 py-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                        />
                    </div>
                </div>

                {/* Category Filter */}
                <div className="flex justify-center gap-3 mb-12 flex-wrap">
                    {['all', 'veg', 'non-veg'].map(category => (
                        <button
                            key={category}
                            onClick={() => filterByCategory(category)}
                            className={`px-6 py-2 rounded-full font-semibold transition-all ${selectedCategory === category
                                ? 'bg-gradient-to-r from-pizza-red to-pizza-orange text-white shadow-lg'
                                : 'bg-pizza-darker border border-pizza-orange/30 hover:bg-pizza-orange/20'
                                }`}
                        >
                            {category === 'all' ? '🍕 All' : category === 'veg' ? '🌱 Vegetarian' : '🍖 Non-Veg'}
                        </button>
                    ))}
                </div>

                {/* Menu Grid */}
                {isLoading ? (
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {[...Array(6)].map((_, i) => (
                            <div key={i} className="glass-dark rounded-2xl p-6 shimmer h-96"></div>
                        ))}
                    </div>
                ) : filteredItems.length === 0 ? (
                    <div className="text-center py-12">
                        <p className="text-2xl text-gray-400">No pizzas found 😢</p>
                        <p className="text-gray-500 mt-2">Try a different search or category</p>
                    </div>
                ) : (
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {filteredItems.map((item, index) => (
                            <motion.div
                                key={item.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="glass-dark rounded-2xl overflow-hidden card-hover group"
                            >
                                {/* Image */}
                                <div className="relative h-48 bg-gradient-to-br from-pizza-orange/20 to-pizza-red/20 flex items-center justify-center overflow-hidden">
                                    <div className="text-8xl group-hover:scale-110 transition-transform">
                                        🍕
                                    </div>
                                    {item.tags.includes('popular') && (
                                        <div className="absolute top-4 right-4 bg-pizza-red text-white px-3 py-1 rounded-full text-sm font-semibold">
                                            🔥 Popular
                                        </div>
                                    )}
                                </div>

                                {/* Content */}
                                <div className="p-6">
                                    <div className="flex justify-between items-start mb-3">
                                        <h3 className="text-2xl font-bold text-white group-hover:text-pizza-orange transition-colors">
                                            {item.name}
                                        </h3>
                                        <div className="text-right">
                                            <div className="text-2xl font-bold text-pizza-orange">
                                                ${item.price}
                                            </div>
                                            <div className="text-xs text-gray-500">medium</div>
                                        </div>
                                    </div>

                                    <div className="flex gap-2 mb-3">
                                        {item.category === 'veg' && (
                                            <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded-full text-xs">
                                                🌱 Veg
                                            </span>
                                        )}
                                        {item.tags.map(tag => (
                                            <span key={tag} className="px-2 py-1 bg-pizza-orange/20 text-pizza-orange rounded-full text-xs">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>

                                    <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                                        {item.description}
                                    </p>

                                    <div className="mb-4">
                                        <div className="text-xs text-gray-500 mb-1">Ingredients:</div>
                                        <div className="flex flex-wrap gap-1">
                                            {item.ingredients.slice(0, 4).map((ing, i) => (
                                                <span key={i} className="text-xs bg-pizza-darker px-2 py-1 rounded">
                                                    {ing}
                                                </span>
                                            ))}
                                            {item.ingredients.length > 4 && (
                                                <span className="text-xs text-gray-500">+{item.ingredients.length - 4} more</span>
                                            )}
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => {
                                            addToCart(item, 'medium');
                                            setToastMessage(`Added ${item.name} to cart!`);
                                            setShowToast(true);
                                            setTimeout(() => setShowToast(false), 3000);
                                        }}
                                        className="w-full btn-primary"
                                    >
                                        Add to Cart
                                    </button>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                )}

                {/* Toast Notification */}
                {showToast && (
                    <motion.div
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 50 }}
                        className="fixed bottom-8 right-8 bg-gradient-to-r from-pizza-red to-pizza-orange text-white px-6 py-4 rounded-xl shadow-2xl z-50"
                    >
                        <div className="flex items-center gap-3">
                            <span className="text-2xl">✓</span>
                            <span className="font-semibold">{toastMessage}</span>
                        </div>
                    </motion.div>
                )}
            </motion.div>
        </div>
    );
}
