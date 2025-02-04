import axios from 'axios';
import { useState, useRef, useEffect } from 'react';

const ChatContainer = ({ 
    isContainerOpen, 
    setIsContainerOpen, 
    messages, 
    setMessages,
    newMessage, 
    setNewMessage,
    handleSendMessage 
}) => {
    const API_URL = 'URL';
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const getAnswer = async (e) => {
        e.preventDefault();
        if (newMessage.trim() && !isLoading) {
            setIsLoading(true);
            
            const userMessage = {
                id: messages.length + 1,
                text: newMessage,
                isBot: false
            };
            
            setMessages([...messages, userMessage]);
            setNewMessage('');

            try {
                const response = await axios.post(API_URL, {
                    query: newMessage
                });

                const botMessage = {
                    id: messages.length + 2,
                    text: response.data,
                    isBot: true
                };

                setMessages(prevMessages => [...prevMessages, botMessage]);

            } catch (error) {
                console.error('API error:', error);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div className={`fixed bottom-5 right-5 z-50 ${isContainerOpen ? 'w-[35vw] h-[70vh] bg-white rounded-xl shadow-lg' : ''}`}>
            {!isContainerOpen && (
                <button 
                    className="absolute bottom-5 right-5 w-12 h-12 rounded-full bg-red-600 text-white text-xl flex items-center justify-center cursor-pointer shadow-md hover:bg-red-700 transition-colors"
                    onClick={() => setIsContainerOpen(true)}
                >
                    💬
                </button>
            )}
            
            {isContainerOpen && (
                <div className="h-full flex flex-col p-5">
                    <div className="pb-4 border-b border-gray-200 flex justify-between items-center">
                        <h2 className="text-lg font-semibold text-gray-800">Assistant Bot</h2>
                        <button 
                            className="w-8 h-8 rounded-full bg-red-600 text-white text-sm flex items-center justify-center cursor-pointer hover:bg-red-700 transition-colors"
                            onClick={() => setIsContainerOpen(false)}
                        >
                            ✕
                        </button>
                    </div>
                    
                    <div className="flex-1 overflow-y-auto py-5 space-y-4">
                        {messages.map(message => (
                            <div 
                                key={message.id} 
                                className={`max-w-[80%] p-3 rounded-2xl whitespace-pre-wrap break-words ${
                                    message.isBot 
                                    ? 'bg-gray-100 self-start' 
                                    : 'bg-red-600 text-white self-end'
                                }`}
                            >
                                {message.text}
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                    
                    <form onSubmit={getAnswer} className="flex gap-3 pt-4 border-t border-gray-200">
                        <input
                            type="text"
                            value={newMessage}
                            onChange={(e) => setNewMessage(e.target.value)}
                            placeholder={isLoading ? "Waiting for response..." : "Type your message..."}
                            className="flex-1 p-2.5 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                            disabled={isLoading}
                        />
                        <button 
                            type="submit"
                            className={`px-5 py-2.5 bg-red-600 text-white rounded hover:bg-red-700 transition-colors ${
                                isLoading ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Waiting for response...' : 'Send'}
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default ChatContainer;
