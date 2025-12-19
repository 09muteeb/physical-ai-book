import React from 'react';
import ChatWidget from '../ChatWidget/ChatWidget';

// Root component that wraps the entire application
const Root = ({children}) => {
  return (
    <>
      {children}
      {/* Chat widget component - will appear on all pages */}
      <ChatWidget backendUrl="http://localhost:8000" position="bottom-right" />
    </>
  );
};

export default Root;