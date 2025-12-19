# Quickstart: Frontend and Backend Integration

## Overview

This guide explains how to integrate the FastAPI-based RAG backend with the Docusaurus frontend to enable user interactions with the chatbot.

## Prerequisites

- Docusaurus project set up and running
- FastAPI RAG backend service running (typically on http://localhost:8000)
- Node.js and npm installed
- Basic knowledge of React and Docusaurus customization

## Setup

### 1. Start the Backend Service

First, ensure your RAG backend is running:

```bash
cd backend
uvicorn rag_agent:app --host 0.0.0.0 --port 8000
```

The backend should be accessible at http://localhost:8000.

### 2. Install Frontend Dependencies

In your Docusaurus project directory:

```bash
npm install
```

### 3. Create the Chat Component

Create the chat widget component that will be integrated into your Docusaurus layout:

```bash
# Create the components directory if it doesn't exist
mkdir src/components/ChatWidget
```

## Implementation Steps

### 1. Create the Chat Widget Component

Create `src/components/ChatWidget/ChatWidget.js`:

```jsx
import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

const ChatWidget = ({ backendUrl = 'http://localhost:8000' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getSelectedText = () => {
    const selection = window.getSelection();
    return selection.toString().trim();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Prepare context with selected text if available
      const selectedText = getSelectedText();
      const context = selectedText ? {
        selected_text: selectedText,
        current_page: window.location.pathname,
        page_title: document.title
      } : null;

      // Prepare query request
      const queryRequest = {
        query: inputValue,
        max_results: 5,
        similarity_threshold: 0.5,
        context: context
      };

      // Add temporary loading message
      const loadingId = 'loading-' + Date.now();
      setMessages(prev => [...prev, {
        id: loadingId,
        text: '',
        sender: 'agent',
        timestamp: new Date().toISOString(),
        isLoading: true
      }]);

      // Send request to backend
      const response = await fetch(`${backendUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(queryRequest)
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();

      // Remove loading message
      setMessages(prev => prev.filter(msg => msg.id !== loadingId));

      // Add agent response
      const agentMessage = {
        id: Date.now().toString(),
        text: data.answer,
        sender: 'agent',
        timestamp: data.timestamp,
        sources: data.sources || []
      };

      setMessages(prev => [...prev, agentMessage]);

    } catch (err) {
      // Remove loading message
      setMessages(prev => prev.filter(msg => msg.isLoading));

      setError('Failed to get response from the RAG agent. Please try again.');
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
    <div className={`chat-widget ${isOpen ? 'open' : 'closed'}`}>
      <button
        className="chat-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? '×' : '💬'}
      </button>

      {isOpen && (
        <div className="chat-container">
          <div className="chat-header">
            <h3>Physical AI Assistant</h3>
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
```

### 2. Create CSS Styling

Create `src/components/ChatWidget/ChatWidget.css`:

```css
.chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.chat-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: #2563eb;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.chat-toggle:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.chat-container {
  width: 380px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: #2563eb;
  color: white;
  padding: 16px;
  flex-shrink: 0;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-welcome {
  text-align: center;
  color: #6b7280;
  font-size: 14px;
  margin-top: 40px;
}

.chat-welcome p {
  margin: 8px 0;
}

.message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  background: #2563eb;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.agent {
  align-self: flex-start;
  background: white;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 4px;
}

.message.error {
  background: #fee2e2;
  color: #dc2626;
  border-color: #fecaca;
}

.sources {
  margin-top: 8px;
  font-size: 12px;
}

.sources small {
  color: #6b7280;
  display: block;
  margin-bottom: 4px;
}

.sources ul {
  margin: 0;
  padding-left: 16px;
  list-style-type: disc;
}

.sources li {
  margin: 2px 0;
}

.sources a {
  color: #2563eb;
  text-decoration: none;
}

.sources a:hover {
  text-decoration: underline;
}

.loading-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.dot {
  width: 8px;
  height: 8px;
  background: #6b7280;
  border-radius: 50%;
  animation: pulse 1.4s infinite both;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-input-form {
  display: flex;
  padding: 16px;
  background: white;
  border-top: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.chat-input-form input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
}

.chat-input-form input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.chat-input-form button {
  margin-left: 8px;
  width: 40px;
  height: 40px;
  border: none;
  background: #2563eb;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
}

.chat-input-form button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.chat-error {
  background: #fee2e2;
  color: #dc2626;
  padding: 8px 16px;
  font-size: 12px;
  text-align: center;
  border-top: 1px solid #fecaca;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .chat-widget {
    bottom: 10px;
    right: 10px;
  }

  .chat-container {
    width: 320px;
    height: 400px;
  }

  .message {
    max-width: 90%;
  }
}
```

### 3. Integrate with Docusaurus Layout

To add the chat widget to all pages, you can use Docusaurus swizzling. First, swizzle the main layout:

```bash
npm run swizzle @docusaurus/theme-classic Footer -- --wrap
```

Then modify the layout to include the chat widget.

Alternatively, create a plugin. Create `src/plugins/ChatWidget/index.js`:

```javascript
import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';

const ChatWidgetPlugin = () => {
  // Only render in browser environment
  if (typeof window !== 'undefined') {
    return <ChatWidget backendUrl={process.env.BACKEND_URL || 'http://localhost:8000'} />;
  }
  return null;
};

export default ChatWidgetPlugin;
```

Add the plugin to your `docusaurus.config.js`:

```javascript
module.exports = {
  // ... other config
  plugins: [
    // ... other plugins
    async function myPlugin(context, options) {
      return {
        name: 'chat-widget-plugin',
        async loadContent() {
          // nothing to load
        },
        async contentLoaded({content, actions}) {
          const {setGlobalData} = actions;
          setGlobalData({});
        },
        configureWebpack(config, isServer, utils) {
          return {
            plugins: [],
          };
        },
      };
    },
  ],
  themes: [
    // ... other themes
  ],
  scripts: [
    // ... other scripts
  ],
  stylesheets: [
    // ... other stylesheets
  ],
};
```

### 4. Alternative: Direct Integration

You can also directly add the ChatWidget to your Docusaurus layout by modifying the theme. Create or modify `src/theme/Layout/index.js`:

```jsx
import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '../../components/ChatWidget/ChatWidget';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatWidget backendUrl="http://localhost:8000" />
    </>
  );
}
```

## Testing the Integration

### 1. Start Both Services

Start your Docusaurus frontend:

```bash
npm run start
```

Start your FastAPI backend:

```bash
cd backend
uvicorn rag_agent:app --host 0.0.0.0 --port 8000
```

### 2. Verify Connection

1. Open your Docusaurus site in a browser
2. Look for the chat widget in the bottom-right corner
3. Click the widget to open it
4. Type a question and submit it
5. Verify that you receive a response from the RAG agent

### 3. Test Features

- **General queries**: Ask questions without selecting text
- **Context queries**: Select text on a page and ask related questions
- **Error handling**: Test with backend offline to verify error messages
- **Loading states**: Verify loading indicators appear during processing

## Configuration Options

### Environment Variables

You can configure the backend URL using environment variables:

```bash
# In your .env file
BACKEND_URL=http://your-backend-domain.com
```

### Customization

The ChatWidget component accepts several props for customization:
- `backendUrl`: URL of the FastAPI backend service
- Additional props can be added as needed for theming and positioning

## Troubleshooting

### Common Issues

**CORS Errors**:
- Ensure your FastAPI backend has CORS configured to allow your frontend domain
- In development, you may need to configure CORS middleware in your FastAPI app

**Backend Not Responding**:
- Verify the backend service is running and accessible
- Check that the backend URL is correctly configured
- Verify network connectivity between frontend and backend

**Text Selection Not Working**:
- Ensure you're properly selecting text before asking context-specific questions
- Check browser console for JavaScript errors

**Chat Widget Not Appearing**:
- Verify the component is properly integrated into your Docusaurus layout
- Check browser console for React errors
- Ensure CSS styles are properly loaded