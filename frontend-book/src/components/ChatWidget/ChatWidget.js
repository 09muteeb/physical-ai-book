import React, { useState, useEffect, useRef } from 'react';
import ChatApi from '@site/src/services/ChatApi';
import { getSelectedText } from '@site/src/utils/textSelection';
import './ChatWidget.css';

const ChatWidget = ({ backendUrl = 'http://localhost:8000', position = 'bottom-right' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const chatApiRef = useRef(null);

  // Calculate position classes based on position prop
  const getPositionClasses = () => {
    const baseClass = 'chat-widget';
    const positionClass = `position-${position}`;
    const openClass = isOpen ? 'open' : 'closed';
    return `${baseClass} ${positionClass} ${openClass}`;
  };

  // Initialize ChatApi instance
  useEffect(() => {
    chatApiRef.current = new ChatApi(backendUrl);
  }, [backendUrl]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Function to handle API call to backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    // Add temporary loading message - declare loadingId outside try block
    const loadingId = 'loading-' + Date.now();
    setMessages(prev => [...prev, {
      id: loadingId,
      text: '',
      sender: 'agent',
      timestamp: new Date().toISOString(),
      isLoading: true
    }]);

    try {
      // Get selected text context if available
      const selectedText = getSelectedText();
      const context = selectedText ? {
        selected_text: selectedText,
        current_page: window.location.pathname,
        page_title: document.title
      } : null;

      // Format the query request
      const queryRequest = {
        query: inputValue,
        max_results: 5,
        similarity_threshold: 0.5,
        context: context
      };

      // Call the backend API
      const response = await chatApiRef.current.query(inputValue, {
        max_results: 5,
        similarity_threshold: 0.5,
        context: context
      });

      // Remove loading message
      setMessages(prev => prev.filter(msg => msg.id !== loadingId));

      // Add agent response
      const agentMessage = {
        id: Date.now().toString(),
        text: response.answer,
        sender: 'agent',
        timestamp: response.timestamp,
        sources: response.sources || []
      };

      setMessages(prev => [...prev, agentMessage]);

    } catch (err) {
      // Remove loading message - use the loadingId that's now in scope
      setMessages(prev => prev.filter(msg => msg.id !== loadingId));

      console.error('Chat error:', err);

      // Add error message to chat
      const errorMessage = {
        id: Date.now().toString(),
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'agent',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={getPositionClasses()}>
      <button
        className="chat-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? '×' : (
          <img
            src="/img/pic-4.png"
            alt="Chat"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              borderRadius: '50%',
              position: 'absolute',
              top: 0,
              left: 0
            }}
          />
        )}
      </button>

      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <h3>Chaty Book</h3>
          </div>

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <p>Ask me anything about the Physical AI book!</p>
                <p>You can also select text on the page and ask questions about it.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
                >
                  <div className="message-content">
                    {message.isLoading ? (
                      <div className="loading-indicator">
                        <div className="dot"></div>
                        <div className="dot"></div>
                        <div className="dot"></div>
                      </div>
                    ) : (
                      <>
                        <p>{message.text}</p>
                        {message.sources && message.sources.length > 0 && (
                          <div className="sources">
                            <small>Sources:</small>
                            <ul>
                              {message.sources.slice(0, 3).map((source, index) => (
                                <li key={index}>
                                  <a href={source} target="_blank" rel="noopener noreferrer">
                                    {new URL(source).pathname.replace('/', '') || 'Home'}
                                  </a>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask about Physical AI..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !inputValue.trim()}>
              {isLoading ? '...' : '→'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;