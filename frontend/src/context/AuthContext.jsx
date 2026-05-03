import { createContext, useContext, useEffect, useState, useCallback } from "react";
import axios from "axios";

// ======================================================
// BACKEND URL PROFISSIONAL
// ======================================================
const getBackendURL = () => {
  const envUrl =
    process.env.REACT_APP_BACKEND_URL ||
    process.env.REACT_APP_API_URL;

  if (envUrl && envUrl.trim() !== "") {
    const cleanUrl = envUrl.replace(/\/+$/, "");
    return cleanUrl.endsWith("/api") ? cleanUrl : `${cleanUrl}/api`;
  }

  return "/api";
};

const BACKEND_URL = getBackendURL();

// ======================================================
// AXIOS INSTANCE
// ======================================================
const api = axios.create({
  baseURL: BACKEND_URL,
  timeout: 15000,
  withCredentials: false,
  headers: {
    "Content-Type": "application/json",
  },
});

// ======================================================
// REQUEST INTERCEPTOR
// ======================================================
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

// ======================================================
// RESPONSE INTERCEPTOR
// ======================================================
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
  (error) => {
    if (error?.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

// ======================================================
// CONTEXT
// ======================================================
const AuthContext = createContext(null);

// ======================================================
// PROVIDER
// ======================================================
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // ======================================================
  // RESTORE SESSION
  // ======================================================
  useEffect(() => {
    try {
      const savedToken = localStorage.getItem("token");
      const savedUser = localStorage.getItem("user");

      if (savedToken) setToken(savedToken);
      if (savedUser) setUser(JSON.parse(savedUser));
    } catch (error) {
      console.error("Erro restaurando sessão:", error);
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    } finally {
      setLoading(false);
    }
  }, []);

  // ======================================================
  // LOGIN
  // ======================================================
  const login = useCallback(async (email, password) => {
    try {
      const response = await api.post("/auth/login", {
        email: email.trim(),
        password,
      });

      const data = response.data || {};

      // backend atual FastAPI
      const authToken =
        data.token ||
        data.access_token ||
        data.jwt ||
        data?.data?.token ||
        null;

      if (!authToken) {
        throw new Error("Token não retornado pela API");
      }

      const userData =
        data.user ||
        data?.data?.user || {
          email,
          nome: "Administrador",
          role: "admin",
        };

      localStorage.setItem("token", authToken);
      localStorage.setItem("user", JSON.stringify(userData));

      setToken(authToken);
      setUser(userData);

      return {
        success: true,
        token: authToken,
        user: userData,
      };
    } catch (error) {
      console.error("Erro no login:", error);

      const message =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        error?.message ||
        "Erro ao realizar login";

      return {
        success: false,
        message,
      };
    }
  }, []);

  // ======================================================
  // LOGOUT
  // ======================================================
  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    setUser(null);
    setToken(null);
  }, []);

  // ======================================================
  // VALIDAR SESSÃO
  // ======================================================
  const validateSession = useCallback(async () => {
    try {
      if (!token) return false;

      const response = await api.get("/me");

      if (response.data) {
        setUser(response.data);
        localStorage.setItem(
          "user",
          JSON.stringify(response.data)
        );
      }

      return true;
    } catch (error) {
      logout();
      return false;
    }
  }, [token, logout]);

  // ======================================================
  // AUTO VALIDAR TOKEN
  // ======================================================
  useEffect(() => {
    if (token) {
      validateSession();
    }
  }, [token, validateSession]);

  // ======================================================
  // VALUE
  // ======================================================
  const value = {
    user,
    token,
    loading,
    backendUrl: BACKEND_URL,
    isAuthenticated: !!token,
    login,
    logout,
    validateSession,
    api,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// ======================================================
// EXPORT API
// ======================================================
export { api };

// ======================================================
// HOOK
// ======================================================
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
};

export default AuthContext;
