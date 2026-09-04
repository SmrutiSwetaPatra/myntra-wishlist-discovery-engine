import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Scale, ArrowLeft } from 'lucide-react';
import { compareService } from '../services/compareService';
import { productService } from '../services/productService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { Button } from '../components/common/Button';
import { ImageGallery } from '../components/common/ImageGallery';

export const Compare = () => {
  const [searchParams] = useSearchParams();
  const idsParam = searchParams.get('ids');
  const ids = idsParam ? idsParam.split(',').map(Number) : [];
  const navigate = useNavigate();
  
  const [comparison, setComparison] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (ids.length < 2) return;
      try {
        setLoading(true);
        setError(null);
        
        // Fetch AI comparison
        const compData = await compareService.compareProducts(ids);
        setComparison(compData);
        
        // Fetch product details
        const prodPromises = ids.map(id => productService.getProduct(id));
        const prods = await Promise.all(prodPromises);
        setProducts(prods);
        
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [idsParam]);

  if (ids.length < 2) {
    return (
      <div style={{ padding: '40px' }}>
        <h1 className="page-title">Compare Products</h1>
        <p className="text-muted">Please select at least 2 items from your wishlist to compare.</p>
        <Button variant="primary" onClick={() => navigate('/wishlist')} style={{ marginTop: '16px' }}>Go to Wishlist</Button>
      </div>
    );
  }

  if (loading) return <LoadingSpinner fullScreen />;
  if (error) return <ErrorState message={error} />;

  return (
    <div>
      <Button variant="ghost" onClick={() => navigate('/wishlist')} style={{ marginBottom: '16px' }}>
        <ArrowLeft size={16} /> Back to Wishlist
      </Button>

      <div className="page-header">
        <h1 className="page-title">Compare Products</h1>
        <p className="page-subtitle">Side-by-side analysis to help you decide.</p>
      </div>
      
      {comparison && (
        <div className="card" style={{ padding: '24px', marginBottom: '32px', backgroundColor: 'var(--color-primary-light)', borderColor: 'var(--color-primary)' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Scale size={20} color="var(--color-primary)" /> AI Recommendation
          </h3>
          <p style={{ lineHeight: '1.6', fontSize: '15px' }}>{comparison.recommendation}</p>
          <div style={{ marginTop: '16px' }}>
            <h4 style={{ fontWeight: '600', marginBottom: '8px' }}>Key Differences:</h4>
            <ul style={{ paddingLeft: '20px', lineHeight: '1.6' }}>
              {comparison.key_differences.map((diff, i) => (
                <li key={i}>{diff}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div style={{ display: 'flex', gap: '24px', overflowX: 'auto', paddingBottom: '16px' }}>
        {products.map(product => (
          <div key={product.id} className="card" style={{ flex: '1 0 300px', minWidth: '300px' }}>
            <div style={{ padding: '16px' }}>
              <div style={{ height: '300px', marginBottom: '16px' }}>
                <ImageGallery images={product.images} />
              </div>
              <h3 style={{ fontSize: '16px', fontWeight: '600' }}>{product.brand}</h3>
              <p style={{ color: 'var(--color-text-muted)', marginBottom: '12px' }}>{product.name}</p>
              <div style={{ fontSize: '18px', fontWeight: '700', marginBottom: '16px' }}>Rs. {product.price}</div>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ padding: '8px', backgroundColor: 'var(--color-surface-hover)', borderRadius: 'var(--radius-sm)' }}>
                  <span style={{ fontSize: '12px', color: 'var(--color-text-muted)', display: 'block' }}>Rating</span>
                  <span style={{ fontWeight: '500' }}>{product.rating} ({product.review_count})</span>
                </div>
                <div style={{ padding: '8px', backgroundColor: 'var(--color-surface-hover)', borderRadius: 'var(--radius-sm)' }}>
                  <span style={{ fontSize: '12px', color: 'var(--color-text-muted)', display: 'block' }}>Fit</span>
                  <span style={{ fontWeight: '500' }}>{product.fit}</span>
                </div>
                <div style={{ padding: '8px', backgroundColor: 'var(--color-surface-hover)', borderRadius: 'var(--radius-sm)' }}>
                  <span style={{ fontSize: '12px', color: 'var(--color-text-muted)', display: 'block' }}>Material</span>
                  <span style={{ fontWeight: '500' }}>{product.material}</span>
                </div>
              </div>
              
              <Button 
                variant="accent" 
                fullWidth 
                style={{ marginTop: '24px' }}
                onClick={() => navigate(`/copilot?productId=${product.id}`)}
              >
                Choose This
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
