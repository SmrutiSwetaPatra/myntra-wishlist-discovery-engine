import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Home, Heart, Sparkles, Scale, LineChart } from 'lucide-react';

export const Navbar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Overview', icon: Home },
    { path: '/wishlist', label: 'Wishlist', icon: Heart },
    { path: '/copilot', label: 'Copilot', icon: Sparkles },
    { path: '/compare', label: 'Compare', icon: Scale },
    { path: '/activity', label: 'Activity', icon: LineChart },
  ];

  return (
    <nav style={{ 
      height: 'var(--header-height)', 
      backgroundColor: 'var(--color-surface)',
      borderBottom: '1px solid var(--color-border-light)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 10
    }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', margin: '0 auto', padding: 0 }}>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-primary)' }}>
          <Sparkles size={24} />
          <span style={{ fontSize: '18px', fontWeight: '700', letterSpacing: '-0.5px' }}>
            Decision Copilot
          </span>
        </div>

        {/* Desktop Navigation */}
        <div style={{ display: 'none' }} className="desktop-nav">
          <ul style={{ display: 'flex', gap: '32px', listStyle: 'none' }}>
            {navItems.map((item) => {
              const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
              return (
                <li key={item.path}>
                  <NavLink 
                    to={item.path}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      color: isActive ? 'var(--color-primary)' : 'var(--color-text-muted)',
                      fontWeight: isActive ? '600' : '500',
                      fontSize: '15px'
                    }}
                  >
                    <item.icon size={18} />
                    {item.label}
                  </NavLink>
                </li>
              );
            })}
          </ul>
        </div>

        <style>{`
          @media (min-width: 768px) {
            .desktop-nav {
              display: block !important;
            }
          }
        `}</style>
      </div>
    </nav>
  );
};
