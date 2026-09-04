import React, { useEffect, useState } from 'react';
import { Heart, Scale } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { wishlistService } from '../services/wishlistService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { EmptyState } from '../components/common/EmptyState';
import { ProductCard } from '../components/common/ProductCard';
import { Button } from '../components/common/Button';

export const Wishlist = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);

  const fetchWishlist = async () => {
    try {
      setLoading(true);
      setError(null);
      const wishlist = await wishlistService.getWishlist();
      setData(wishlist);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  const toggleSelect = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(pid => pid !== id) : [...prev, id]
    );
  };

  const handleCompare = () => {
    if (selectedIds.length < 2) {
      alert('Please select at least 2 items to compare.');
      return;
    }
    navigate(`/compare?ids=${selectedIds.join(',')}`);
  };

  if (loading) return <LoadingSpinner fullScreen />;
  if (error) return <ErrorState message={error} onRetry={fetchWishlist} />;

  const items = data?.items || [];

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="page-title">My Wishlist</h1>
          <p className="page-subtitle">Your saved items, ready for a decision.</p>
        </div>
        {items.length > 0 && (
          <Button variant="primary" onClick={handleCompare} disabled={selectedIds.length < 2}>
            <Scale size={18} /> Compare Selected ({selectedIds.length})
          </Button>
        )}
      </div>

      {items.length === 0 ? (
        <EmptyState 
          icon={Heart}
          title="Your wishlist is empty"
          description="Save items you like and let the Decision Copilot help you choose the best one."
        />
      ) : (
        <div className="grid grid-cols-4">
          {items.map(item => (
            <ProductCard 
              key={item.id} 
              product={item.product} 
              selectable 
              selected={selectedIds.includes(item.product.id)}
              onSelect={toggleSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
};
