import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Sparkles, AlertCircle } from 'lucide-react';
import { wishlistService } from '../services/wishlistService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { ProductCard } from '../components/common/ProductCard';
import { Button } from '../components/common/Button';

export const Home = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchOverview = async () => {
    try {
      setLoading(true);
      setError(null);
      // Fetch wishlist to build overview factual stats
      const wishlist = await wishlistService.getWishlist();
      setData(wishlist);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  if (loading) return <LoadingSpinner fullScreen />;
  if (error) return <ErrorState message={error} onRetry={fetchOverview} />;

  const itemsCount = data?.items?.length || 0;
  // Factual metric: all items in wishlist represent a pending decision
  const pendingDecisionsCount = itemsCount;
  
  // Show up to 4 recent items
  const recentItems = data?.items ? data.items.slice(0, 4) : [];

  return (
    <div>
      <div className="page-header text-center" style={{ marginBottom: '40px', marginTop: '20px' }}>
        <h1 className="page-title">Welcome Back</h1>
        <p className="page-subtitle">Here is an overview of your saved items.</p>
        <div style={{ marginTop: '16px' }}>
          <Button variant="primary" onClick={() => navigate('/discover')}>Discover Products</Button>
        </div>
      </div>

      <div className="grid grid-cols-2" style={{ marginBottom: '48px' }}>
        <div className="card text-center" style={{ padding: '24px' }}>
          <div style={{ display: 'inline-flex', padding: '12px', backgroundColor: 'rgba(255, 20, 147, 0.1)', color: 'var(--color-secondary)', borderRadius: '50%', marginBottom: '16px' }}>
            <Heart size={28} />
          </div>
          <h2 style={{ fontSize: '36px', fontWeight: '700', marginBottom: '4px' }}>{itemsCount}</h2>
          <p className="text-muted" style={{ fontWeight: '500' }}>Saved Items</p>
        </div>

        <div className="card text-center" style={{ padding: '24px' }}>
          <div style={{ display: 'inline-flex', padding: '12px', backgroundColor: 'rgba(138, 43, 226, 0.1)', color: 'var(--color-primary)', borderRadius: '50%', marginBottom: '16px' }}>
            <Sparkles size={28} />
          </div>
          <h2 style={{ fontSize: '36px', fontWeight: '700', marginBottom: '4px' }}>{pendingDecisionsCount}</h2>
          <p className="text-muted" style={{ fontWeight: '500' }}>Pending Decisions</p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '700' }}>Recently Saved</h2>
        <Button variant="ghost" onClick={() => navigate('/wishlist')}>View All</Button>
      </div>

      {recentItems.length > 0 ? (
        <div className="grid grid-cols-4">
          {recentItems.map(item => (
            <ProductCard key={item.id} product={item.product} />
          ))}
        </div>
      ) : (
        <div className="card" style={{ padding: '40px', textAlign: 'center' }}>
          <p className="text-muted">No items in your wishlist yet.</p>
        </div>
      )}
    </div>
  );
};
