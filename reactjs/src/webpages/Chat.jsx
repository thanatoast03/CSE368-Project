import React, {useState, useRef, useEffect } from 'react';
import './chat.css';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const chatInitialized = useRef(false);

    const initializeChat = async () => {
        setIsLoading(true);
        try {
            const response = await fetch('http://localhost:5001/chatInitialize', {
                method: 'GET'
            });
        } catch (error) {
            const errorMessage = { 
                text: "Sorry, an error occurred.",
                sender: 'bot'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if(!chatInitialized.current){
            const initialMessage = {
                text: "Hello! I am a bot designed to help with picking computer science or computer engineering classes. Let's get started with some questions. What is your year and your major?",
                sender: 'bot'
            };
            setMessages([initialMessage]);
            initializeChat();
            chatInitialized.current = true;
        }
    }, [messages.length]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const getRoleDescription = () => {
        return "Class Picker Helper Bot - Here at Your Service!";
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { text: input, sender: 'user' };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:5001/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userMessage)
            });
            const data = await response.json();
            const botMessage = { 
                text: data.text,
                sender: 'bot'
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = { 
                text: "Sorry, an error occurred.",
                sender: 'bot'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className='background'>
            <div className="chat-container">
                {/* Bot info card */}
                <div className="bot-info-card">
                    <div className="bot-info-content">
                        <div className="bot-details">
                            <h2>Class Picker Helper Bot</h2>
                            <p>{getRoleDescription()}</p>
                        </div>
                    </div>
                </div>
            
                {/* Chat messages */}
                <div className="messages-area">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`message ${message.sender}`}
                        >
                            <div className="message-bubble">
                                {message.text}
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="loading-message">Coming up with a response</div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            
                {/* Input form */}
                <form onSubmit={handleSubmit} className="chat-input-form">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Say something..."
                        disabled={isLoading}
                        className="chat-input"
                        style={{
                            backgroundColor: '#333',
                            color: '#fff',
                            border: '1px solid #555',
                            padding: '10px',
                            borderRadius: '4px'
                        }}
                    />
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="chat-submit"
                    >
                    Send
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Chat;
