import React from 'react';
import { LineChart } from 'lucide-react';
import { EmptyState } from '../components/common/EmptyState';

export const Insights = () => {
  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Insights</h1>
        <p className="page-subtitle">Your personal shopping trends.</p>
      </div>
      
      <EmptyState 
        icon={LineChart}
        title="Insights Dashboard"
        description="View trends based on your actual wishlist data. Coming in Phase 2B."
      />
    </div>
  );
};
