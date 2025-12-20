'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { sendChatMessage, type ChatMessage, type ChatResponse } from '@/lib/api-client';

interface Message {
    role: 'user' | 'agent';
    content: string;
    tool_used?: string;
    timestamp?: string;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'agent',
            content: '👋 Hi! I\'m AGENT-X, your intelligent pizza assistant. How can I help you today?',
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            role: 'user',
            content: input,
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const chatData: ChatMessage = {
                message: input,
                user_id: 'web_user_' + Math.random().toString(36).substr(2, 9),
                conversation_history: messages.map(m => ({
                    role: m.role,
                    content: m.content
                }))
            };

            const response: ChatResponse = await sendChatMessage(chatData);

            const agentMessage: Message = {
                role: 'agent',
                content: response.reply,
                tool_used: response.tool_used,
                timestamp: response.timestamp
            };

            setMessages(prev => [...prev, agentMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, {
                role: 'agent',
                content: '❌ Sorry, I encountered an error. Please try again.',
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-dark rounded-3xl shadow-2xl overflow-hidden"
            >
                {/* Chat Header */}
                <div className="bg-gradient-to-r from-pizza-red to-pizza-orange p-6">
                    <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                        🤖 Chat with AGENT-X
                        <span className="text-sm font-normal text-white/80">● Online</span>
                    </h1>
                    <p className="text-white/80 text-sm mt-1">
                        Ask me anything about our menu, delivery, or place an order!
                    </p>
                </div>

                {/* Messages Container */}
                <div className="h-[500px] overflow-y-auto p-6 space-y-4 bg-pizza-darker/50">
                    <AnimatePresence>
                        {messages.map((message, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.3 }}
                                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[75%] rounded-2xl p-4 ${message.role === 'user'
                                            ? 'bg-gradient-to-r from-pizza-orange to-pizza-red text-white'
                                            : 'glass border border-pizza-orange/30'
                                        }`}
                                >
                                    <div className="whitespace-pre-wrap">{message.content}</div>
                                    {message.tool_used && (
                                        <div className="text-xs mt-2 opacity-70">
                                            🛠️ Tool: {message.tool_used}
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {/* Typing Indicator */}
                    {isLoading && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex justify-start"
                        >
                            <div className="glass border border-pizza-orange/30 rounded-2xl p-4">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-pizza-orange rounded-full typing-dot"></div>
                                    <div className="w-2 h-2 bg-pizza-orange rounded-full typing-dot"></div>
                                    <div className="w-2 h-2 bg-pizza-orange rounded-full typing-dot"></div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-6 bg-pizza-dark border-t border-pizza-orange/30">
                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your message..."
                            className="flex-1 bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-pizza-orange"
                            disabled={isLoading}
                        />
                        <motion.button
                            onClick={handleSend}
                            disabled={isLoading || !input.trim()}
                            className="btn-primary px-6"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            {isLoading ? '...' : 'Send'}
                        </motion.button>
                    </div>

                    {/* Quick Actions */}
                    <div className="flex flex-wrap gap-2 mt-4">
                        <button
                            onClick={() => setInput('Show me all pizzas')}
                            className="text-sm px-3 py-1 bg-pizza-darker rounded-full border border-pizza-orange/30 hover:bg-pizza-orange/20 transition-colors"
                        >
                            📋 Show menu
                        </button>
                        <button
                            onClick={() => setInput('I want something spicy and cheesy')}
                            className="text-sm px-3 py-1 bg-pizza-darker rounded-full border border-pizza-orange/30 hover:bg-pizza-orange/20 transition-colors"
                        >
                            🌶️ Recommend spicy
                        </button>
                        <button
                            onClick={() => setInput('What are your delivery hours?')}
                            className="text-sm px-3 py-1 bg-pizza-darker rounded-full border border-pizza-orange/30 hover:bg-pizza-orange/20 transition-colors"
                        >
                            ⏰ Delivery hours
                        </button>
                        <button
                            onClick={() => setInput('What payment methods do you accept?')}
                            className="text-sm px-3 py-1 bg-pizza-darker rounded-full border border-pizza-orange/30 hover:bg-pizza-orange/20 transition-colors"
                        >
                            💳 Payment info
                        </button>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
