import { fetchApi } from './api';

export const compareService = {
  compareProducts: (productIds) => fetchApi('/compare/', {
    method: 'POST',
    body: JSON.stringify({ product_ids: productIds })
  }),
};
