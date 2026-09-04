import React, { useEffect, useState } from 'react';
import { Activity as ActivityIcon, Clock, CheckCircle2, ShoppingBag, Eye, Heart, Sparkles, Scale, Trash2 } from 'lucide-react';
import { analyticsService } from '../services/analyticsService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorState } from '../components/common/ErrorState';
import { EmptyState } from '../components/common/EmptyState';
import { productService } from '../services/productService';

export const Activity = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch raw events
        const data = await analyticsService.getInsights();
        
        // Enrich events with product data if they have a product_id
        const enrichedEvents = await Promise.all((data || []).map(async (event) => {
          if (event.product_id) {
            try {
              const product = await productService.getProduct(event.product_id);
              return { ...event, product };
            } catch (err) {
              return event;
            }
          }
          return event;
        }));
        
        // Sort descending by timestamp
        enrichedEvents.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        setEvents(enrichedEvents);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchActivity();
  }, []);

  const getEventMeta = (eventType) => {
    switch (eventType) {
      case 'wishlist_item_added':
        return { icon: Heart, color: 'var(--color-success)', label: 'Product saved' };
      case 'wishlist_item_removed':
        return { icon: Trash2, color: 'var(--color-warning)', label: 'Product removed' };
      case 'wishlist_item_viewed':
        return { icon: Eye, color: 'var(--color-text-main)', label: 'Product viewed' };
      case 'decision_copilot_opened':
        return { icon: Sparkles, color: 'var(--color-primary)', label: 'Copilot opened' };
      case 'decision_factor_selected':
        return { icon: Clock, color: 'var(--color-primary)', label: 'Decision factor explored' };
      case 'compare_alternatives_clicked':
      case 'comparison_started':
        return { icon: Scale, color: 'var(--color-secondary)', label: 'Comparison started' };
      case 'comparison_completed':
        return { icon: Scale, color: 'var(--color-secondary)', label: 'Comparison completed' };
      case 'decision_made':
      case 'ready_to_buy_clicked':
        return { icon: CheckCircle2, color: 'var(--color-success)', label: 'Decision made' };
      case 'added_to_cart':
        return { icon: ShoppingBag, color: 'var(--color-success)', label: 'Added to cart' };
      default:
        return { icon: ActivityIcon, color: 'var(--color-text-muted)', label: eventType };
    }
  };

  const formatDate = (dateString) => {
    const d = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit'
    }).format(d);
  };

  if (loading) return <LoadingSpinner fullScreen />;
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', paddingBottom: '40px' }}>
      <div className="page-header">
        <h1 className="page-title">Activity</h1>
        <p className="page-subtitle">Your recent shopping decisions and history.</p>
      </div>

      {events.length === 0 ? (
        <EmptyState 
          icon={ActivityIcon}
          title="No activity yet"
          description="Start browsing and using the Decision Copilot to see your timeline."
        />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {events.map((event) => {
            const meta = getEventMeta(event.event_type);
            const Icon = meta.icon;
            return (
              <div key={event.id} className="card" style={{ padding: '16px', display: 'flex', gap: '16px', alignItems: 'center' }}>
                <div style={{ padding: '12px', backgroundColor: 'var(--color-surface-hover)', borderRadius: '50%', color: meta.color }}>
                  <Icon size={20} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <h4 style={{ fontWeight: '600', fontSize: '15px' }}>{meta.label}</h4>
                    <span style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>{formatDate(event.timestamp)}</span>
                  </div>
                  {event.product && (
                    <div style={{ fontSize: '14px', color: 'var(--color-text-muted)' }}>
                      {event.product.brand} - {event.product.name}
                    </div>
                  )}
                  {event.event_data && (
                    <div style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginTop: '4px', fontStyle: 'italic' }}>
                      Details: {JSON.stringify(event.event_data)}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
