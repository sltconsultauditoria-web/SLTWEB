import axios from "axios";

// Usa a variável REACT_APP_BACKEND_URL definida no .env
const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para capturar erros de rede
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("Erro na requisição:", error.message);
    return Promise.reject(error);
  }
);

export default api;

