import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL || process.env.API_URL || '';

if (!baseURL) {
  throw new Error('API_URL não configurado');
}

const api = axios.create({
  baseURL,
});

export default api;
