import { createContext, useContext, useEffect, useState, useCallback } from "react";
import axios from "axios";

// ==============================
// Axios instance
// ==============================
const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// ==============================
// Context
// ==============================
const AuthContext = createContext(null);

// ==============================
// Provider
// ==============================
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // ==============================
  // Load session
  // ==============================
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (storedToken) {
      setToken(storedToken);
      api.defaults.headers.common.Authorization = `Bearer ${storedToken}`;
    }

    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem("user");
      }
    }

    setLoading(false);
  }, []);

  // ==============================
  // LOGIN
  // ==============================
  const login = useCallback(async (email, password) => {
    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      const data = response.data;

      // suporte a diferentes formatos de API
      const authToken = data?.data?.token || data?.token;
      const userData = data?.data?.user || data?.user;

      if (!authToken) {
        throw new Error("Token não retornado pela API");
      }

      localStorage.setItem("token", authToken);
      api.defaults.headers.common.Authorization = `Bearer ${authToken}`;
      setToken(authToken);

      if (userData) {
        localStorage.setItem("user", JSON.stringify(userData));
        setUser(userData);
      }

      return data;
    } catch (error) {
      console.error("LOGIN ERROR:", error?.response?.data || error.message);
      throw error;
    }
  }, []);

  // ==============================
  // LOGOUT
  // ==============================
  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    delete api.defaults.headers.common.Authorization;

    setUser(null);
    setToken(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!token,
        login,
        logout,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

// ==============================
// Hook
// ==============================
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
};