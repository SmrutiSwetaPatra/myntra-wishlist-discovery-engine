import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Badge } from './Badge';
import { Button } from './Button';
import { Star, Sparkles } from 'lucide-react';

export const ProductCard = ({ product, selectable, selected, onSelect }) => {
  const navigate = useNavigate();
  
  // Use the first image from the array, or a placeholder if missing
  const imageUrl = product.images && product.images.length > 0 
    ? product.images[0] 
    : `https://placehold.co/400x500/f8f8f8/8a2be2?text=${encodeURIComponent(product.category || 'Product')}`;

  const handleCardClick = () => {
    if (selectable && onSelect) {
      onSelect(product.id);
    } else {
      navigate(`/products/${product.id}`);
    }
  };

  return (
    <div className={`card ${selected ? 'selected' : ''}`} style={{ cursor: 'pointer', position: 'relative' }} onClick={handleCardClick}>
      {selectable && (
        <div style={{ position: 'absolute', top: '12px', left: '12px', zIndex: 2 }}>
          <input 
            type="checkbox" 
            checked={selected} 
            readOnly 
            style={{ width: '20px', height: '20px', cursor: 'pointer' }}
          />
        </div>
      )}
      <div 
        style={{ 
          height: '240px', 
          backgroundColor: '#f2f2f2',
          backgroundImage: `url('${imageUrl}')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />
      <div className="card-body" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        
        <div>
          <h4 style={{ fontSize: '14px', color: 'var(--color-text-muted)', fontWeight: '600' }}>
            {product.brand}
          </h4>
          <h3 style={{ fontSize: '16px', fontWeight: '500', color: 'var(--color-text-main)', marginTop: '4px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {product.name}
          </h3>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '18px', fontWeight: '700' }}>Rs. {product.price}</span>
          {product.rating && (
            <Badge variant="outline" className="badge-outline">
              <Star size={12} style={{ marginRight: '4px', color: 'var(--color-warning)', fill: 'var(--color-warning)' }} />
              {product.rating} | {product.review_count}
            </Badge>
          )}
        </div>
        
        <div style={{ marginTop: '8px' }}>
          <Button 
            variant="accent" 
            fullWidth 
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/copilot?productId=${product.id}`);
            }}
          >
            <Sparkles size={16} /> Help me decide
          </Button>
        </div>
      </div>
    </div>
  );
};
