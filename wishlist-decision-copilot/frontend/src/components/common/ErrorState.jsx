import React from 'react';
import { Button } from './Button';
import { AlertCircle } from 'lucide-react';

export const ErrorState = ({ message = 'Something went wrong', onRetry }) => {
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '48px',
    textAlign: 'center',
    backgroundColor: 'var(--color-surface)',
    borderRadius: 'var(--radius-md)',
    border: '1px solid var(--color-border-light)'
  };

  return (
    <div style={containerStyle}>
      <AlertCircle size={48} color="var(--color-error)" style={{ marginBottom: '16px' }} />
      <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px' }}>Oops!</h3>
      <p style={{ color: 'var(--color-text-muted)', marginBottom: '24px' }}>{message}</p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
};
