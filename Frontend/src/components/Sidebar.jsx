import React, { useState, useEffect } from 'react';
import '../styles/Sidebar.css';

const Sidebar = ({ 
  isCollapsed, 
  onToggleCollapse, 
  onBackToChat, 
  onFAQSelect,
  isMobile,
  isMobileMenuOpen,
  onMobileMenuClose
}) => {
  const [isFAQOpen, setIsFAQOpen] = useState(false);
  const [departments, setDepartments] = useState([]);
  const [faqData, setFaqData] = useState({});

  const loadDepartments = async () => {
    try {
      console.log('Starting to load departments...');
      const res = await fetch('/data/faq_data.json');
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

  // Load data and auto-open FAQ when mobile menu opens
  useEffect(() => {
    console.log('Mobile menu effect:', { isMobile, isMobileMenuOpen, departmentsLength: departments.length });
    if (isMobile && isMobileMenuOpen) {
      console.log('Mobile menu opened, ensuring data loaded...');
      loadDepartments();
      // Auto-open FAQ section on mobile for better UX
      setIsFAQOpen(true);
    }
  }, [isMobile, isMobileMenuOpen]);

  const handleToggleCollapse = () => {
    onToggleCollapse();
    if (!isCollapsed) {
      setIsFAQOpen(false);
    }
  };

  const handleFAQToggle = () => {
    if (isCollapsed) {
      onToggleCollapse();
    }
    setIsFAQOpen(!isFAQOpen);
  };

  const handleBackToChatClick = () => {
    onBackToChat();
    // Close mobile menu after navigation
    if (isMobile) {
      onMobileMenuClose();
    }
  };


  const handleDepartmentClick = (dept) => {
    onFAQSelect(dept, faqData[dept]);
    // Close mobile menu after selection
    if (isMobile) {
      onMobileMenuClose();
    }
  };

  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : 'expanded'} ${isMobile && isMobileMenuOpen ? 'mobile-open' : ''}`}>
      <button 
        className="sidebar-toggle" 
        onClick={handleToggleCollapse}
        title="Collapse sidebar"
      >
        <span className="material-icons">chevron_left</span>
      </button>


      <button 
        className="sidebar-back-btn" 
        onClick={handleBackToChatClick}
        title="Back to Chat"
      >
        <span className="material-icons">chat_bubble_outline</span>
        <span className="label">BACK TO CHAT</span>
      </button>

      <button 
        className="faq-toggle" 
        onClick={handleFAQToggle}
        title="FAQs"
      >
        <span className="material-icons">help_outline</span>
        <span className="label">FAQs</span>
        <span className={`material-icons arrow ${isFAQOpen ? 'rotated' : ''}`}>
          expand_more
        </span>
      </button>

      <nav className={`sidebar-nav ${isFAQOpen ? 'open' : ''}`}>
        {departments.length === 0 ? (
          <div style={{ padding: '10px', textAlign: 'center', color: 'var(--muted)' }}>
            <span className="material-icons" style={{ fontSize: '16px', display: 'block', marginBottom: '5px' }}>
              loading
            </span>
            <span className="label">Loading...</span>
          </div>
        ) : (
          departments.map((dept) => (
            <button
              key={dept.name}
              onClick={() => handleDepartmentClick(dept.name)}
              title={dept.name}
            >
              <span className="material-icons">{dept.icon}</span>
              <span className="label">{dept.name.toUpperCase()}</span>
            </button>
          ))
        )}
      </nav>
    </aside>
  );
};

export default Sidebar;
