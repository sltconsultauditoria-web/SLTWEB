import { createContext, useContext, useEffect, useState, useCallback } from "react";
import axios from "axios";

// ==============================
// Axios config
// ==============================
const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
} );

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

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    if (storedToken) {
      setToken(storedToken);
      api.defaults.headers.common.Authorization = `Bearer ${storedToken}`;
    }
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  // --- FUNÇÃO DE LOGIN CORRIGIDA ---
  const login = useCallback(async (email, password) => {
    const response = await api.post("/auth/login", { email, password });
    
    // 'responseData' é o objeto completo retornado pela API: { success, message, data: { token, user } }
    const responseData = response.data;

    // 1. Acessar o token corretamente
    const authToken = responseData.data?.token;
    
    // 2. Acessar o usuário corretamente
    const userData = responseData.data?.user;

    if (!authToken) {
      throw new Error("Token não foi retornado pela API");
    }

    // Armazena o token no localStorage e no cabeçalho do axios
    localStorage.setItem("token", authToken);
    api.defaults.headers.common.Authorization = `Bearer ${authToken}`;
    setToken(authToken);

    // Se os dados do usuário existirem, armazena no localStorage e no estado
    if (userData) {
      localStorage.setItem("user", JSON.stringify(userData));
      setUser(userData);
    }

    return responseData;
  }, []);
  // ---------------------------------

  const logout = useCallback(() => {
    localStorage.clear();
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
