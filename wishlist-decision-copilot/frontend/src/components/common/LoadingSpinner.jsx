import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingSpinner = ({ message = 'Loading...', fullScreen = false }) => {
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '48px',
    minHeight: fullScreen ? '60vh' : 'auto',
    color: 'var(--color-text-muted)'
  };

  return (
    <div style={containerStyle}>
      <Loader2 size={32} className="spinner" style={{ animation: 'spin 1s linear infinite', marginBottom: '16px', color: 'var(--color-primary)' }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      {message && <p>{message}</p>}
    </div>
  );
};
