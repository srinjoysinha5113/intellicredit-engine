import React from 'react';
import { useTheme } from '../hooks/ThemeProvider';
import StaggeredMenu from './StaggeredMenu';
import '../styles/Header.css';

const Header = ({ onBackToChat, onNewChat, isMobile, onMobileMenuToggle, staggeredMenuProps }) => {
  const { theme, toggleTheme } = useTheme();

  const logoSrc = theme === 'dark' 
    ? '/assets/jindal-logo-dark.png' 
    : '/assets/jindal-logo-light.png';

  const themeIcon = theme === 'dark' ? 'light_mode' : 'dark_mode';

  return (
    <header className="header">
      <div className="header-left">
        {staggeredMenuProps && (
          <div className="header-menu">
            <StaggeredMenu {...staggeredMenuProps} />
          </div>
        )}
        
        <img 
          src={logoSrc} 
          className="logo" 
          alt="Jindal Logo" 
        />
        <div className="separator"></div>
        <div>
          <div className="title">Jindal Assistant</div>
          <div className="subtitle">Internal Knowledge System</div>
        </div>
      </div>

      <div className="header-right">
        <button className="back-btn" onClick={onBackToChat} title="Back to Chat">
          <span className="material-icons">chat_bubble_outline</span>
        </button>

        <button className="new-chat-btn" onClick={onNewChat} title="New Chat">
          <span className="material-icons">add_comment</span>
        </button>

        <button className="icon-btn" onClick={toggleTheme} title="Toggle theme">
          <span className="material-icons">{themeIcon}</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
