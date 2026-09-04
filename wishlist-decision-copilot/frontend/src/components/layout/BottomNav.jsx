import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Home, Heart, Sparkles, Scale, LineChart } from 'lucide-react';

export const BottomNav = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Overview', icon: Home },
    { path: '/wishlist', label: 'Wishlist', icon: Heart },
    { path: '/copilot', label: 'Copilot', icon: Sparkles },
    { path: '/compare', label: 'Compare', icon: Scale },
    { path: '/activity', label: 'Activity', icon: LineChart },
  ];

  return (
    <>
      <nav className="bottom-nav">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
          return (
            <NavLink 
              key={item.path}
              to={item.path}
              className="nav-item"
              style={{ color: isActive ? 'var(--color-primary)' : 'var(--color-text-light)' }}
            >
              <item.icon size={24} />
              <span style={{ fontSize: '11px', marginTop: '4px', fontWeight: isActive ? '600' : '400' }}>
                {item.label}
              </span>
            </NavLink>
          );
        })}
      </nav>

      <style>{`
        .bottom-nav {
          display: flex;
          justify-content: space-around;
          align-items: center;
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          height: var(--bottom-nav-height);
          background-color: var(--color-surface);
          border-top: 1px solid var(--color-border-light);
          padding-bottom: env(safe-area-inset-bottom);
          z-index: 10;
        }
        .nav-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          flex: 1;
        }
        @media (min-width: 768px) {
          .bottom-nav {
            display: none;
          }
        }
      `}</style>
    </>
  );
};
