import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShoppingBag, Heart, Shield, Undo2, Star, Sparkles } from 'lucide-react';
import { productService } from '../services/productService';
import { wishlistService } from '../services/wishlistService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { Button } from '../components/common/Button';
import { ImageGallery } from '../components/common/ImageGallery';
import { Badge } from '../components/common/Badge';

export const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [wishlisting, setWishlisting] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await productService.getProduct(id);
        setProduct(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  const handleWishlist = async () => {
    try {
      setWishlisting(true);
      await wishlistService.addItem(id);
      alert('Added to Wishlist!');
    } catch (err) {
      alert(err.message);
    } finally {
      setWishlisting(false);
    }
  };

  const handleCopilot = () => {
    navigate(`/copilot?productId=${id}`);
  };

  if (loading) return <LoadingSpinner fullScreen />;
  if (error) return <ErrorState message={error} />;
  if (!product) return <ErrorState message="Product not found" />;

  return (
    <div className="product-detail">
      <Button variant="ghost" onClick={() => navigate(-1)} style={{ marginBottom: '16px' }}>
        <Undo2 size={16} /> Back
      </Button>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
        <div>
          <ImageGallery images={product.images} />
        </div>

        <div>
          <div style={{ marginBottom: '24px' }}>
            <h2 style={{ fontSize: '24px', fontWeight: '700', color: 'var(--color-text-main)' }}>{product.brand}</h2>
            <h1 style={{ fontSize: '20px', fontWeight: '500', color: 'var(--color-text-muted)', marginBottom: '12px' }}>{product.name}</h1>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <Badge variant="outline">
                <Star size={14} style={{ marginRight: '4px', fill: 'var(--color-warning)', color: 'var(--color-warning)' }} />
                {product.rating} | {product.review_count} Ratings
              </Badge>
            </div>

            <div style={{ display: 'flex', alignItems: 'baseline', gap: '12px' }}>
              <span style={{ fontSize: '24px', fontWeight: '700' }}>Rs. {product.price}</span>
              {product.original_price && (
                <span style={{ fontSize: '16px', color: 'var(--color-text-muted)', textDecoration: 'line-through' }}>
                  Rs. {product.original_price}
                </span>
              )}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '32px' }}>
            <Button variant="primary" fullWidth size="lg">
              <ShoppingBag size={20} /> Add to Cart
            </Button>
            <div style={{ display: 'flex', gap: '12px' }}>
              <Button variant="secondary" fullWidth onClick={handleWishlist} disabled={wishlisting}>
                <Heart size={20} /> Save
              </Button>
              <Button variant="accent" fullWidth onClick={handleCopilot}>
                <Sparkles size={20} /> Help me decide
              </Button>
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: '24px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px' }}>Product Details</h3>
            <p style={{ color: 'var(--color-text-muted)', lineHeight: '1.6', marginBottom: '16px' }}>
              {product.description}
            </p>
            
            <ul style={{ color: 'var(--color-text-muted)', display: 'flex', flexDirection: 'column', gap: '8px', paddingLeft: '20px' }}>
              <li><strong>Fit:</strong> {product.fit}</li>
              <li><strong>Material:</strong> {product.material}</li>
              <li><strong>Color:</strong> {product.color}</li>
            </ul>
          </div>
          
          <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: '24px', marginTop: '24px', display: 'flex', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-text-muted)' }}>
              <Shield size={20} />
              <span style={{ fontSize: '14px' }}>100% Original Products</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
