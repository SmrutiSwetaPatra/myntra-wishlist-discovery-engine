import { fetchApi } from './api';

export const analyticsService = {
  trackEvent: (eventType, productId = null, eventData = null) => fetchApi('/analytics/events', {
    method: 'POST',
    body: JSON.stringify({
      event_type: eventType,
      product_id: productId,
      event_data: eventData
    })
  }),
  getInsights: () => fetchApi('/analytics/insights'),
};
