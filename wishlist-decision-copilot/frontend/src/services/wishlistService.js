import { fetchApi } from './api';

export const wishlistService = {
  getWishlist: () => fetchApi('/wishlist/'),
  addItem: (productId) => fetchApi('/wishlist/items', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId })
  }),
  removeItem: (productId) => fetchApi(`/wishlist/items/${productId}`, {
    method: 'DELETE'
  }),
};
