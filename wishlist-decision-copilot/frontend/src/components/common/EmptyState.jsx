import React from 'react';
import { Button } from './Button';

export const EmptyState = ({ 
  icon: Icon, 
  title, 
  description, 
  actionLabel, 
  onAction 
}) => {
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '64px 24px',
    textAlign: 'center',
    backgroundColor: 'var(--color-surface)',
    borderRadius: 'var(--radius-md)',
    border: '1px dashed var(--color-border)'
  };

  return (
    <div style={containerStyle}>
      {Icon && (
        <div style={{ padding: '16px', backgroundColor: 'rgba(138,43,226,0.1)', borderRadius: '50%', marginBottom: '24px', color: 'var(--color-primary)' }}>
          <Icon size={32} />
        </div>
      )}
      <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '12px' }}>{title}</h3>
      <p style={{ color: 'var(--color-text-muted)', maxWidth: '400px', marginBottom: '32px' }}>
        {description}
      </p>
      {actionLabel && onAction && (
        <Button variant="accent" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};
