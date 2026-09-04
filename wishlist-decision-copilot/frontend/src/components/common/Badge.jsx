import React from 'react';
import '../../styles/components.css';

export const Badge = ({ children, variant = 'outline', className = '' }) => {
  const baseClass = 'badge';
  const variantClass = `badge-${variant}`;
  
  return (
    <span className={`${baseClass} ${variantClass} ${className}`}>
      {children}
    </span>
  );
};
