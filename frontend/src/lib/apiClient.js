import axios from "axios";

export const resolveApiBaseUrl = () => {
  const envUrl = process.env.REACT_APP_API_URL;
  if (!envUrl || envUrl.trim() === "") {
    throw new Error("REACT_APP_API_URL não configurado");
  }
  const cleanUrl = envUrl.replace(/\/+$/, "");
  return cleanUrl.endsWith("/api") ? cleanUrl.slice(0, -4) : cleanUrl;
};

export const createApiClient = () => {
  const api = axios.create({
    baseURL: resolveApiBaseUrl(),
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

      const url = config.url || "";
      if (url.startsWith("/") && !url.startsWith("/api/") && url !== "/health" && url !== "/docs") {
        config.url = `/api${url}`;
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
