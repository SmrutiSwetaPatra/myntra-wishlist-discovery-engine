import { fetchApi } from './api';

export const decisionService = {
  analyzeProduct: (productId) => fetchApi('/decision/analyze', {
    method: 'POST',
    body: JSON.stringify({ product_id: Number(productId) })
  }),
};
