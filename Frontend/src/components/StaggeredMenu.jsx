import React, { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import '../styles/StaggeredMenu.css';

const StaggeredMenu = ({
  position = 'right',
  items = [],
  displayItemNumbering = false,
  menuButtonColor = '#ffffff',
  openMenuButtonColor = '#fff',
  changeMenuColorOnOpen = true,
  colors = ['#B19EEF', '#5227FF'],
  logoUrl = '',
  accentColor = '#5227FF',
  onMenuOpen = () => {},
  onMenuClose = () => {}
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);
  const itemsRef = useRef([]);
  const buttonRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Animate menu items in with stagger
      gsap.fromTo(itemsRef.current,
        { x: position === 'right' ? 100 : -100, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.5, stagger: 0.05, ease: 'power3.out' }
      );
      
      onMenuOpen();
    } else {
      // Animate menu items out
      gsap.to(itemsRef.current, {
        x: position === 'right' ? 100 : -100,
        opacity: 0,
        duration: 0.3,
        stagger: 0.03,
        ease: 'power2.in'
      });
      
      onMenuClose();
    }
  }, [isOpen, position, onMenuOpen, onMenuClose]);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleItemClick = (item) => {
    if (item.action) {
      item.action();
    } else if (item.link) {
      if (item.link.startsWith('http')) {
        window.open(item.link, '_blank');
      } else {
        window.location.href = item.link;
      }
    }
    setIsOpen(false);
  };

  return (
    <div className={`staggered-menu staggered-menu--${position}`} ref={menuRef}>
      {/* Menu Button */}
      <button
        ref={buttonRef}
        className={`icon-btn staggered-menu__button ${isOpen ? 'open' : ''}`}
        onClick={toggleMenu}
      >
        {logoUrl ? (
          <img src={logoUrl} alt="Menu" className="staggered-menu__logo" />
        ) : (
          <div className="staggered-menu__hamburger">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
      </button>

      {/* Menu Items */}
      <div className={`staggered-menu__overlay ${isOpen ? 'open' : ''}`}>
        <nav className="staggered-menu__nav">
          {items.map((item, index) => (
            <button
              key={index}
              ref={el => itemsRef.current[index] = el}
              className="staggered-menu__item"
              onClick={() => handleItemClick(item)}
              aria-label={item.ariaLabel || item.label}
              style={{
                '--accent-color': accentColor,
                '--gradient-start': colors[0],
                '--gradient-end': colors[1]
              }}
            >
              {displayItemNumbering && (
                <span className="staggered-menu__item-number">
                  {String(index + 1).padStart(2, '0')}
                </span>
              )}
              <span className="staggered-menu__item-text">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default StaggeredMenu;
