import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Sparkles, CheckCircle2, AlertTriangle, ArrowRight, ShoppingBag, Scale, ChevronRight } from 'lucide-react';
import { productService } from '../services/productService';
import { decisionService } from '../services/decisionService';
import { analyticsService } from '../services/analyticsService';
import { EmptyState } from '../components/common/EmptyState';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';

export const DecisionCopilot = () => {
  const [searchParams] = useSearchParams();
  const productId = searchParams.get('productId');
  const navigate = useNavigate();

  const [product, setProduct] = useState(null);
  const [decision, setDecision] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeChip, setActiveChip] = useState(null);
  const [cartSuccess, setCartSuccess] = useState(false);
  const [isDeciding, setIsDeciding] = useState(false);

  useEffect(() => {
    if (!productId) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Load product and decision data concurrently
        const [prodData, decData] = await Promise.all([
          productService.getProduct(productId),
          decisionService.analyzeProduct(productId)
        ]);
        
        setProduct(prodData);
        setDecision(decData);

        // Track copilot opened
        analyticsService.trackEvent('decision_copilot_opened', productId);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [productId]);

  if (!productId) {
    return (
      <div style={{ marginTop: '40px' }}>
        <EmptyState 
          icon={Sparkles}
          title="Select a Product"
          description="Go to your wishlist and select a product you need help deciding on."
          actionLabel="Go to Wishlist"
          onAction={() => navigate('/wishlist')}
        />
      </div>
    );
  }

  if (loading) return <LoadingSpinner fullScreen />;
  if (error) return <ErrorState message={error} />;
  if (!product || !decision) return <ErrorState message="Could not load copilot data" />;

  const imageUrl = product.images && product.images.length > 0 ? product.images[0] : '';

  const handleChipSelect = (chip) => {
    setActiveChip(activeChip === chip ? null : chip);
    if (activeChip !== chip) {
      analyticsService.trackEvent('decision_factor_selected', productId, { factor: chip });
    }
  };

  const handleDecision = (type) => {
    setIsDeciding(true);
    analyticsService.trackEvent('decision_made', productId, { decision: type });
    
    if (type === 'buy') {
      analyticsService.trackEvent('ready_to_buy_clicked', productId);
      setTimeout(() => {
        setIsDeciding(false);
      }, 500);
    } else {
      analyticsService.trackEvent('keep_comparing_clicked', productId);
      navigate('/wishlist');
    }
  };

  const handleAddToCart = () => {
    analyticsService.trackEvent('added_to_cart', productId);
    setCartSuccess(true);
  };

  const chips = [
    { id: 'price_value', label: 'Price / Value', content: `At Rs. ${product.price}, ${decision.supporting_info.value_analysis || 'this offers good value.'}` },
    { id: 'fit_size', label: 'Fit / Size', content: `Fit profile: ${product.fit}. Sizes available: ${product.sizes?.join(', ') || 'Various'}` },
    { id: 'quality', label: 'Quality', content: `Material: ${product.material}. ${decision.supporting_info.quality_analysis || 'Quality seems standard for this brand.'}` },
    { id: 'reviews', label: 'Reviews', content: `Rated ${product.rating} stars from ${product.review_count} users. ${decision.supporting_info.review_analysis || 'Generally positive feedback.'}` }
  ];

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', paddingBottom: '80px' }}>
      <div className="page-header text-center">
        <h1 className="page-title" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          <Sparkles color="var(--color-primary)" /> Decision Copilot
        </h1>
        <p className="page-subtitle">Your personalized shopping assistant</p>
      </div>
      
      {/* 1. Product Header */}
      <div className="card" style={{ display: 'flex', gap: '20px', padding: '20px', marginBottom: '24px' }}>
        <div style={{ width: '120px', height: '160px', borderRadius: 'var(--radius-md)', overflow: 'hidden', flexShrink: 0 }}>
          <img src={imageUrl} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h2 style={{ fontSize: '18px', fontWeight: '700', color: 'var(--color-text-main)' }}>{product.brand}</h2>
          <h3 style={{ fontSize: '16px', color: 'var(--color-text-muted)', marginBottom: '12px' }}>{product.name}</h3>
          <div style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>Rs. {product.price}</div>
          <Badge variant="outline" style={{ alignSelf: 'flex-start' }}>
            ★ {product.rating} ({product.review_count} reviews)
          </Badge>
        </div>
      </div>

      {/* 2. The Quick Take */}
      <div className="card" style={{ padding: '24px', marginBottom: '24px', backgroundColor: 'var(--color-surface-hover)' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>The Quick Take</h3>
        <p style={{ lineHeight: '1.6', fontSize: '15px' }}>{decision.ai_summary}</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
        {/* 3. Why consider it */}
        <div className="card" style={{ padding: '24px', borderColor: 'var(--color-success)', backgroundColor: 'rgba(52, 199, 89, 0.05)' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-success)' }}>
            <CheckCircle2 size={18} /> Why consider it
          </h3>
          <ul style={{ display: 'flex', flexDirection: 'column', gap: '12px', padding: 0, margin: 0, listStyle: 'none' }}>
            {decision.decision_factors.map((factor, i) => (
              <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '14px', lineHeight: '1.5' }}>
                <span style={{ color: 'var(--color-success)', marginTop: '2px' }}>•</span> {factor}
              </li>
            ))}
          </ul>
        </div>

        {/* 4. Things to consider */}
        <div className="card" style={{ padding: '24px', borderColor: 'var(--color-warning)', backgroundColor: 'rgba(255, 149, 0, 0.05)' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: '#d97706' }}>
            <AlertTriangle size={18} /> Things to consider
          </h3>
          <ul style={{ display: 'flex', flexDirection: 'column', gap: '12px', padding: 0, margin: 0, listStyle: 'none' }}>
            {decision.concerns.map((concern, i) => (
              <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '14px', lineHeight: '1.5' }}>
                <span style={{ color: '#d97706', marginTop: '2px' }}>•</span> {concern}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 5 & 6. What are you unsure about? & Compare */}
      <div style={{ marginBottom: '40px' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>What are you unsure about?</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
          {chips.map(chip => (
            <button 
              key={chip.id}
              onClick={() => handleChipSelect(chip.id)}
              style={{
                padding: '10px 16px',
                borderRadius: 'var(--radius-full)',
                border: `1px solid ${activeChip === chip.id ? 'var(--color-primary)' : 'var(--color-border)'}`,
                backgroundColor: activeChip === chip.id ? 'var(--color-primary-light)' : 'var(--color-surface)',
                color: activeChip === chip.id ? 'var(--color-primary)' : 'var(--color-text-main)',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              {chip.label}
            </button>
          ))}
          <button 
            onClick={() => {
              analyticsService.trackEvent('compare_alternatives_clicked', productId);
              navigate(`/compare?ids=${productId}`);
            }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '10px 16px',
              borderRadius: 'var(--radius-full)',
              border: '1px solid var(--color-border)',
              backgroundColor: 'var(--color-surface)',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            <Scale size={16} /> Compare alternatives
          </button>
        </div>

        {activeChip && (
          <div className="card" style={{ padding: '20px', marginTop: '16px', backgroundColor: 'var(--color-surface-hover)', animation: 'fadeIn 0.3s ease' }}>
            <p style={{ lineHeight: '1.6' }}>{chips.find(c => c.id === activeChip)?.content}</p>
          </div>
        )}
      </div>

      {/* 7 & 9. Final decision support */}
      <div className="card" style={{ padding: '32px', textAlign: 'center', borderTop: '4px solid var(--color-primary)' }}>
        <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '12px' }}>Ready to decide?</h3>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: '24px', maxWidth: '500px', margin: '0 auto 24px', lineHeight: '1.6' }}>
          {decision.recommendation}
        </p>
        
        {cartSuccess ? (
          <div style={{ padding: '16px', backgroundColor: 'rgba(52, 199, 89, 0.1)', color: 'var(--color-success)', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
            <CheckCircle2 size={20} /> Successfully added to bag!
          </div>
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', gap: '16px' }}>
            <Button variant="secondary" size="lg" onClick={() => handleDecision('wait')} disabled={isDeciding}>
              Keep comparing
            </Button>
            <Button variant="primary" size="lg" onClick={() => handleDecision('buy')} disabled={isDeciding}>
              <ShoppingBag size={18} /> I'm ready to buy
            </Button>
          </div>
        )}
        
        {!cartSuccess && (
          <div style={{ marginTop: '24px', display: cartSuccess ? 'none' : 'block' }}>
            {isDeciding && (
              <div style={{ marginTop: '16px' }}>
                <Button variant="accent" size="lg" onClick={handleAddToCart} fullWidth style={{ maxWidth: '300px', margin: '0 auto' }}>
                  Demo: Add to Cart <ChevronRight size={18} />
                </Button>
                <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', marginTop: '8px' }}>This is a simulated action. No payment required.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
