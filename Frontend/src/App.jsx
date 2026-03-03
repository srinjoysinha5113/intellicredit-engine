import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './hooks/ThemeProvider';
import Header from './components/Header';
import StaggeredMenu from './components/StaggeredMenu';
import ChatArea from './components/ChatArea';
import { marked } from 'marked';
import './styles/variables.css';
import './styles/App.css';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [draftInput, setDraftInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentView, setCurrentView] = useState('chat'); // 'chat' or 'faq'
  const [faqMessages, setFaqMessages] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [faqData, setFaqData] = useState({});
  const [sessionId, setSessionId] = useState(null); // Session management
  
  // Mobile state
  const [isMobile, setIsMobile] = useState(false);

  // Load FAQ departments on component mount
  useEffect(() => {
    const fetchData = async () => {
      await loadDepartments();
    };
    fetchData();
  }, []);

  const loadDepartments = async () => {
    try {
      console.log('Starting to load departments...');
      const res = await fetch(`${import.meta.env.VITE_FAQ_DATA_PATH}`);
      const data = await res.json();
      console.log('FAQ data loaded:', data);
      setFaqData(data);
      const deptNames = Object.keys(data);
      
      const icons = {
        hr: "badge",
        admin: "admin_panel_settings",
        it: "computer",
        mines: "terrain",
        chp: "factory",
      };

      const departmentsWithIcons = deptNames.map(dept => ({
        name: dept,
        icon: icons[dept.toLowerCase()] || "folder"
      }));
      
      console.log('Departments processed:', departmentsWithIcons);
      setDepartments(departmentsWithIcons);
    } catch (err) {
      console.error("Error loading FAQ data:", err);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      await loadDepartments();
    };
    fetchData();
  }, []);

  // Mobile detection
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= parseInt(import.meta.env.VITE_MOBILE_BREAKPOINT));
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Load chat history from sessionStorage on component mount
  useEffect(() => {
    const savedHistory = sessionStorage.getItem(import.meta.env.VITE_CHAT_HISTORY_KEY);
    const savedDraft = sessionStorage.getItem(import.meta.env.VITE_DRAFT_INPUT_KEY);
    const savedView = sessionStorage.getItem(import.meta.env.VITE_CURRENT_VIEW_KEY);
    const savedProcessing = sessionStorage.getItem(import.meta.env.VITE_PROCESSING_KEY);
    const savedSessionId = sessionStorage.getItem(import.meta.env.VITE_SESSION_ID_KEY);
    
    let shouldShowWarning = false;
    
    if (savedHistory) {
      try {
        setChatHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to parse chat history:', e);
      }
    }
    
    if (savedDraft) {
      setDraftInput(savedDraft);
    }
    
    if (savedView) {
      setCurrentView(savedView);
    }
    
    if (savedSessionId) {
      setSessionId(savedSessionId);
    }
    
    if (savedProcessing === 'true') {
      setIsProcessing(false); // Reset to allow new queries
      shouldShowWarning = true;
      console.log('Previous processing was interrupted by refresh');
    }

    // Add warning message after loading history
    if (shouldShowWarning) {
      setTimeout(() => {
        setChatHistory(prev => [...prev, {
          type: 'bot',
          content: '⚠️ Your previous request was interrupted by page refresh. Please try again.'
        }]);
      }, 100); // Small delay to ensure history is loaded first
    }
  }, []);

  // Save chat history to sessionStorage when it changes
  useEffect(() => {
    if (chatHistory.length > 0) {
      sessionStorage.setItem(import.meta.env.VITE_CHAT_HISTORY_KEY, JSON.stringify(chatHistory));
    }
  }, [chatHistory]);

  // Save draft input to sessionStorage when it changes
  useEffect(() => {
    sessionStorage.setItem(import.meta.env.VITE_DRAFT_INPUT_KEY, draftInput);
  }, [draftInput]);

  // Save current view to sessionStorage when it changes
  useEffect(() => {
    sessionStorage.setItem(import.meta.env.VITE_CURRENT_VIEW_KEY, currentView);
  }, [currentView]);

  // Save session ID to sessionStorage when it changes
  useEffect(() => {
    if (sessionId) {
      sessionStorage.setItem(import.meta.env.VITE_SESSION_ID_KEY, sessionId);
    }
  }, [sessionId]);

  // Save processing state to sessionStorage when it changes
  useEffect(() => {
    sessionStorage.setItem(import.meta.env.VITE_PROCESSING_KEY, isProcessing.toString());
  }, [isProcessing]);

  const isChatEmpty = chatHistory.length === 0 && currentView === 'chat';

  const handleBackToChat = () => {
    setCurrentView('chat');
    setFaqMessages([]);
    setDraftInput('');
  };

  const handleNewChat = () => {
    setChatHistory([]);
    setCurrentView('chat');
    setFaqMessages([]);
    setDraftInput('');
    setIsProcessing(false);
    setSessionId(null); // Reset session for new chat
    // Clear sessionStorage for fresh start
    sessionStorage.removeItem(import.meta.env.VITE_CHAT_HISTORY_KEY);
    sessionStorage.removeItem(import.meta.env.VITE_DRAFT_INPUT_KEY);
    sessionStorage.removeItem(import.meta.env.VITE_SESSION_ID_KEY);
    sessionStorage.setItem(import.meta.env.VITE_CURRENT_VIEW_KEY, 'chat');
    sessionStorage.setItem(import.meta.env.VITE_PROCESSING_KEY, 'false');
  };

  const handleFAQSelect = (dept, questions) => {
    // Save current draft input before switching to FAQ
    setDraftInput('');
    
    const faqChatMessages = [
      { type: 'bot', content: `<strong>${dept.toUpperCase()} FAQs</strong>` }
    ];

    questions.forEach((q) => {
      faqChatMessages.push({ type: 'user', content: q.q });
      faqChatMessages.push({ type: 'bot', content: q.a });
    });

    setFaqMessages(faqChatMessages);
    setCurrentView('faq');
  };

  const handleSendMessage = async (message) => {
    setIsProcessing(true);

    // Add user message to history
    const userMessage = { type: 'user', content: message };
    setChatHistory(prev => [...prev, userMessage]);

    // Add bot placeholder for streaming
    const botPlaceholder = { type: 'bot', content: 'Thinking...' };
    const placeholderIndex = chatHistory.length + 1;
    setChatHistory(prev => [...prev, botPlaceholder]);

    try {
      // Generate or get session ID
      let currentSessionId = sessionId;
      if (!currentSessionId) {
        currentSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        setSessionId(currentSessionId);
      }

      // Use streaming endpoint
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message,
          session_id: currentSessionId
        })
      });

      if (!response.ok) {
        throw new Error('Backend error');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              switch (data.type) {
                case 'start':
                  // Update session ID if provided
                  if (data.session_id && data.session_id !== currentSessionId) {
                    setSessionId(data.session_id);
                  }
                  break;
                  
                case 'chunk':
                  // Stream the content
                  fullResponse += data.content;
                  setChatHistory(prev => {
                    const newHistory = [...prev];
                    newHistory[placeholderIndex] = {
                      type: 'bot',
                      content: marked.parse(fullResponse)
                    };
                    return newHistory;
                  });
                  break;
                  
                case 'end':
                  // Final response with sources
                  fullResponse = data.content;
                  setChatHistory(prev => {
                    const newHistory = [...prev];
                    newHistory[placeholderIndex] = {
                      type: 'bot',
                      content: marked.parse(fullResponse)
                    };
                    return newHistory;
                  });
                  break;
                  
                case 'error':
                  throw new Error(data.message);
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError);
            }
          }
        }
      }
      
      // Clear draft input after successful send
      setDraftInput('');
      
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = { 
        type: 'bot', 
        content: 'Sorry, I encountered an error. Please try again.' 
      };
      
      // Replace placeholder with error message
      setChatHistory(prev => {
        const newHistory = [...prev];
        newHistory[placeholderIndex] = errorMessage;
        return newHistory;
      });
      
      // Clear draft input on error too
      setDraftInput('');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleInputChange = (value) => {
    setDraftInput(value);
  };

  // Get current messages based on view
  const currentMessages = currentView === 'faq' ? faqMessages : chatHistory;

  // Create menu items for StaggeredMenu
  const menuItems = [
    { label: 'Back to Chat', ariaLabel: 'Go back to chat', link: null, action: handleBackToChat },
    { label: 'New Chat', ariaLabel: 'Start a new chat', link: null, action: handleNewChat }
  ];

  // Add FAQ departments to menu
  departments.forEach((dept, index) => {
    menuItems.push({
      label: dept.name.toUpperCase(),
      ariaLabel: `View ${dept.name} FAQs`,
      link: null,
      action: () => handleFAQSelect(dept.name, faqData[dept.name])
    });
  });

  const staggeredMenuProps = {
    position: 'left',
    items: menuItems,
    displayItemNumbering: false,
    menuButtonColor: "var(--text)",
    openMenuButtonColor: "var(--primary)",
    changeMenuColorOnOpen: true,
    colors: ['var(--primary)', 'var(--text)'],
    logoUrl: "",
    accentColor: "var(--primary)",
    onMenuOpen: () => console.log('Menu opened'),
    onMenuClose: () => console.log('Menu closed')
  };

  return (
    <ThemeProvider>
      <div style={{ height: '100vh', position: 'relative', display: 'flex', flexDirection: 'column' }}>
        <Header 
          onBackToChat={handleBackToChat}
          onNewChat={handleNewChat}
          isMobile={isMobile}
          staggeredMenuProps={staggeredMenuProps}
        />
        
        <div className="app">
          <ChatArea
            chatHistory={currentMessages}
            isEmpty={isChatEmpty}
            draftInput={draftInput}
            onSendMessage={handleSendMessage}
            onInputChange={handleInputChange}
            isProcessing={isProcessing}
            showInput={currentView === 'chat'}
          />
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
