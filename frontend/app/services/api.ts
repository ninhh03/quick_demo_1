import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3001', // đổi thành URL deploy nếu có
});

export const getProducts = async (params?: any) => {
  // thêm t: Date.now() để tránh cache 304
  const { data } = await api.get('/products', { 
    params: { ...params, t: Date.now() } 
  });
  return data;
};

export const getProductById = async (id: string) => {
  const { data } = await api.get(`/products/${id}`);
  return data;
};
