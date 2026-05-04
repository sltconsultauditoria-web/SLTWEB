import axios from "axios";

export const API_URL =
  process.env.REACT_APP_API_URL || "https://sltweb.onrender.com/api";

console.log("API BASE URL:", API_URL);

export const resolveApiBaseUrl = () => API_URL;

export const createApiClient = () => {
  const api = axios.create({
    baseURL: API_URL,
    timeout: 15000,
    headers: {
      "Content-Type": "application/json",
    },
  });

  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    },
    (error) => Promise.reject(error)
  );

  api.interceptors.response.use(
    (response) => {
      const payload = response.data;
      if (
        payload &&
        typeof payload === "object" &&
        Object.prototype.hasOwnProperty.call(payload, "success") &&
        Object.prototype.hasOwnProperty.call(payload, "data")
      ) {
        response.data = payload.data;
      }
      return response;
    },
    (error) => Promise.reject(error)
  );

  return api;
};

const api = createApiClient();

export default api;
