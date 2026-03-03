import React from 'react';
import '../styles/TypingIndicator.css';

const TypingIndicator = () => {
  return (
    <div className="message bot">
      <div className="typing-indicator">
        <div className="typing-dots">
          <span className="typing-dot"></span>
          <span className="typing-dot"></span>
          <span className="typing-dot"></span>
        </div>
        <span className="typing-text">AI is thinking...</span>
      </div>
    </div>
  );
};

export default TypingIndicator;
