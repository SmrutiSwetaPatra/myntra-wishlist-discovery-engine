import { fetchApi } from './api';

export const productService = {
  getProducts: (params = {}) => fetchApi('/products/', {}, params),
  getProduct: (id) => fetchApi(`/products/${id}`),
};
