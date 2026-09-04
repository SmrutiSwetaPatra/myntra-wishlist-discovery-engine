import React from 'react';
import '../../styles/components.css';

export const Button = ({ 
  children, 
  variant = 'primary', 
  fullWidth = false, 
  onClick, 
  disabled, 
  type = 'button',
  className = ''
}) => {
  const baseClass = 'btn';
  const variantClass = `btn-${variant}`;
  const widthClass = fullWidth ? 'btn-full' : '';
  
  return (
    <button
      type={type}
      className={`${baseClass} ${variantClass} ${widthClass} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
