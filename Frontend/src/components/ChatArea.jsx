import React, { useState, useRef, useEffect } from 'react';
import '../styles/ChatArea.css';

const ChatArea = ({ 
  chatHistory, 
  isEmpty, 
  draftInput,
  onSendMessage,
  onInputChange,
  isProcessing,
  showInput = true 
}) => {
  const [inputValue, setInputValue] = useState(draftInput);
  const [expandedItems, setExpandedItems] = useState(new Set());
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    setInputValue(draftInput);
  }, [draftInput]);

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleSend = async () => {
    if (!inputValue.trim() || isProcessing) return;
    
    const message = inputValue;
    setInputValue('');
    onInputChange('');

    // Reset textarea height.
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    
    await onSendMessage(message);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    onInputChange(value);
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  // FAQ helpers
  const isFAQMode = !showInput && chatHistory.some(msg => msg.type === 'bot' && msg.content.includes('<strong>'));
  const faqTitle = isFAQMode ? chatHistory[0]?.content : '';
  const faqPairs = [];
  if (isFAQMode) {
    for (let i = 1; i < chatHistory.length; i += 2) {
      const q = chatHistory[i];
      const a = chatHistory[i + 1];
      if (q?.type === 'user' && a?.type === 'bot') {
        faqPairs.push({ question: q.content, answer: a.content });
      }
    }
  }

  const toggleExpanded = (index) => {
    setExpandedItems(prev => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <main className={`chat-canvas ${isEmpty ? 'empty-chat' : ''} ${!showInput ? 'faq-view' : ''}`}>
      {isEmpty && (
        <div className="chat-welcome">How can I help you today?</div>
      )}

      <div className="chat-messages">
        {isFAQMode ? (
          <div className="faq-list">
            <div className="faq-title" dangerouslySetInnerHTML={{ __html: faqTitle }} />
            {faqPairs.map((pair, idx) => (
              <div key={idx} className="faq-item">
                <button
                  className="faq-question"
                  onClick={() => toggleExpanded(idx)}
                >
                  <span className="faq-question-text">{pair.question}</span>
                  <span className={`material-icons faq-arrow ${expandedItems.has(idx) ? 'expanded' : ''}`}>
                    expand_more
                  </span>
                </button>
                <div className={`faq-answer ${expandedItems.has(idx) ? 'expanded' : ''}`}>
                  <div dangerouslySetInnerHTML={{ __html: pair.answer }} />
                </div>
              </div>
            ))}
          </div>
        ) : (
          chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.type === 'bot' ? (
                <div dangerouslySetInnerHTML={{ __html: msg.content }} />
              ) : (
                msg.content
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {showInput && (
        <div className="chat-input">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your question…"
            rows={1}
            disabled={isProcessing}
          />
          <button 
            onClick={handleSend}
            disabled={isProcessing || !inputValue.trim()}
          >
            <span className="material-icons">send</span>
          </button>
        </div>
      )}

      <footer className="chat-footer">
        <p>This property belongs to JPL.</p>
        <p>This model may make mistakes. Please verify critical information.</p>
      </footer>
    </main>
  );
};

export default ChatArea;
