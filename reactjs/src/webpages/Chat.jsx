import React, { useState, useEffect, useRef } from 'react';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [userMessage, setUserMessage] = useState('');
    const [typingMessage, setTypingMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const fetchChatHistory = async () => {
        const response = await fetch('http://localhost:5000/chat/history', {
            method: 'GET',
            credentials: 'include',
        });
        const data = await response.json();
        if (response.ok) {
            setMessages(data.chatHistory);
        } else {
            console.error(data.error);
        }
    };

    useEffect(() => {
        fetchChatHistory();
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async (e) => {
        e.preventDefault();
        setIsTyping(true);
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ message: userMessage }),
        });

        if (response.ok) {
            const data = await response.json();
            setMessages((prev) => [
                ...prev,
                { user_message: userMessage, ai_response: data.response },
            ]);
            setUserMessage('');
            setTypingMessage(data.response);
            setIsTyping(false);
        } else {
            console.error('Error:', response.status, response.statusText);
        }
    };

    return (
        <div>
            <h1>Chat with AI</h1>
            <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid #ccc', padding: '10px' }}>
                {messages.map((msg, index) => (
                    <div key={index} style={{ marginBottom: '10px' }}>
                        <strong>You:</strong> {msg.user_message}
                        <br />
                        <strong>AI:</strong> {msg.ai_response}
                    </div>
                ))}
                {isTyping && (
                    <div style={{ marginBottom: '10px' }}>
                        <strong>AI:</strong> {typingMessage}
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <form onSubmit={sendMessage} style={{ marginTop: '10px' }}>
                <input
                    type="text"
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                    required
                    style={{ width: '80%', padding: '10px' }}
                />
                <button type="submit" style={{ padding: '10px' }}>Send</button>
            </form>
        </div>
    );
};

export default Chat;


