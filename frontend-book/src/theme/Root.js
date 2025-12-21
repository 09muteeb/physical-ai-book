import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';

// Root component that wraps the entire application
const Root = ({children}) => {
  return (
    <>
      {children}
      {/* Chat widget component - will appear on all pages */}
      {/* Use relative path for production, localhost for development */}
      <ChatWidget
        backendUrl={typeof window !== 'undefined' && window.location.hostname !== 'localhost'
          ? '/api'
          : 'http://localhost:8000'}
        position="bottom-right"
      />
    </>
  );
};

export default Root;