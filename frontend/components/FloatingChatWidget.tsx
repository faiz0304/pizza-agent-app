'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState, useRef, useEffect } from 'react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export default function FloatingChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'assistant',
            content: 'Hi! I\'m AGENT-X, your pizza ordering assistant. How can I help you today?',
            timestamp: new Date()
        }
    ]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async () => {
        if (!inputMessage.trim() || isLoading) return;

        const userMessage: Message = {
            role: 'user',
            content: inputMessage,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

            // Prepare conversation history for context
            const history = messages.slice(0, -1).map(msg => ({
                role: msg.role,
                content: msg.content
            }));

            console.log('Sending chat request to:', `${apiUrl}/chatbot/`);

            const response = await fetch(`${apiUrl}/chatbot/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: 'web_user',
                    message: inputMessage,
                    conversation_history: history
                })
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('API error:', errorText);
                throw new Error(`API returned ${response.status}`);
            }

            const data = await response.json();
            console.log('API response:', data);

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.reply || 'I apologize, I couldn\'t process that request.',
                timestamp: new Date()
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Chat error:', error);
            const errorMessage: Message = {
                role: 'assistant',
                content: 'Sorry, I\'m having trouble connecting. Please try again.',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <>
            {/* Floating Chat Button */}
            <AnimatePresence>
                {!isOpen && (
                    <motion.button
                        initial={{ scale: 0, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0, opacity: 0 }}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => setIsOpen(true)}
                        className="fixed bottom-6 right-6 z-50 w-16 h-16 bg-gradient-to-r from-pizza-red to-pizza-orange rounded-full shadow-2xl flex items-center justify-center text-3xl cursor-pointer hover:shadow-pizza-orange/50"
                    >
                        🤖
                    </motion.button>
                )}
            </AnimatePresence>

            {/* Chat Widget */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 100, scale: 0.8 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 100, scale: 0.8 }}
                        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                        className="fixed bottom-6 right-6 z-50 w-96 h-[600px] glass-dark rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-pizza-orange/30"
                    >
                        {/* Header */}
                        <div className="bg-gradient-to-r from-pizza-red to-pizza-orange p-4 flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <span className="text-2xl">🤖</span>
                                <div>
                                    <h3 className="font-bold text-white">AI Assistant</h3>
                                    <p className="text-xs text-white/80">Agent-X Pizza</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
                            >
                                ✕
                            </button>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4">
                            {messages.map((msg, index) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div
                                        className={`max-w-[80%] rounded-2xl px-4 py-2 ${msg.role === 'user'
                                            ? 'bg-gradient-to-r from-pizza-red to-pizza-orange text-white'
                                            : 'bg-pizza-darker text-gray-100'
                                            }`}
                                    >
                                        <p className="text-sm">{msg.content}</p>
                                        <p className="text-xs opacity-60 mt-1">
                                            {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}
                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="bg-pizza-darker rounded-2xl px-4 py-2">
                                        <div className="flex gap-1">
                                            <span className="w-2 h-2 bg-pizza-orange rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                                            <span className="w-2 h-2 bg-pizza-orange rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                                            <span className="w-2 h-2 bg-pizza-orange rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input */}
                        <div className="p-4 border-t border-pizza-orange/30">
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={inputMessage}
                                    onChange={(e) => setInputMessage(e.target.value)}
                                    onKeyPress={handleKeyPress}
                                    placeholder="Ask me anything..."
                                    disabled={isLoading}
                                    className="flex-1 bg-pizza-darker border border-pizza-orange/30 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-pizza-orange disabled:opacity-50"
                                />
                                <button
                                    onClick={handleSendMessage}
                                    disabled={!inputMessage.trim() || isLoading}
                                    className="bg-gradient-to-r from-pizza-red to-pizza-orange text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Send
                                </button>
                            </div>
                            <p className="text-xs text-gray-500 mt-2 text-center">
                                Press Enter to send
                            </p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}
