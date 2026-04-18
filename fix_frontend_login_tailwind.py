import os

print("============================================================")
print("FIX FRONTEND LOGIN + TAILWIND SLTWEB")
print("============================================================")

FRONTEND_PATH = "frontend/src"
SERVICES_PATH = os.path.join(FRONTEND_PATH, "services")

# ---------------------------------------------------
# 1. FIX LOGIN PAGE
# ---------------------------------------------------
login_path = os.path.join(FRONTEND_PATH, "pages", "LoginPage.jsx")

login_code = """import { useState } from "react";
import api from "../services/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await api.post("/login", {
        email,
        password
      });

      const data = res.data?.data;

      if (!data?.token) {
        throw new Error("Token não recebido");
      }

      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      window.location.href = "/dashboard";

    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
        "Falha no login. Verifique suas credenciais."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-xl shadow-md w-full max-w-md"
      >
        <h1 className="text-2xl font-bold mb-6 text-center">
          Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
          required
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded"
          disabled={loading}
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>

        {error && (
          <p className="text-red-500 mt-4 text-center">
            {error}
          </p>
        )}
      </form>
    </div>
  );
}
"""

os.makedirs(os.path.dirname(login_path), exist_ok=True)
with open(login_path, "w", encoding="utf-8") as f:
    f.write(login_code)

print("✅ LoginPage corrigido")

# ---------------------------------------------------
# 2. FIX API (AXIOS)
# ---------------------------------------------------
api_path = os.path.join(SERVICES_PATH, "api.js")

api_code = """import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL + "/api",
});

export default api;
"""

os.makedirs(SERVICES_PATH, exist_ok=True)
with open(api_path, "w", encoding="utf-8") as f:
    f.write(api_code)

print("✅ API service corrigido")

# ---------------------------------------------------
# 3. FIX TAILWIND INDEX.CSS
# ---------------------------------------------------
index_css_path = os.path.join(FRONTEND_PATH, "index.css")

tailwind_css = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""

with open(index_css_path, "w", encoding="utf-8") as f:
    f.write(tailwind_css)

print("✅ Tailwind index.css corrigido")

# ---------------------------------------------------
# 4. FIX TAILWIND CONFIG
# ---------------------------------------------------
tailwind_config_path = "frontend/tailwind.config.js"

tailwind_config = """module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
"""

with open(tailwind_config_path, "w", encoding="utf-8") as f:
    f.write(tailwind_config)

print("✅ Tailwind config corrigido")

# ---------------------------------------------------
# 5. FIX .ENV
# ---------------------------------------------------
env_path = "frontend/.env"

env_content = """REACT_APP_API_URL=http://localhost:8000
"""

with open(env_path, "w", encoding="utf-8") as f:
    f.write(env_content)

print("✅ .env corrigido")

print("============================================================")
print("🎯 FRONTEND TOTALMENTE CORRIGIDO")
print("============================================================")
print("AGORA EXECUTE:")
print("cd frontend")
print("npm start")
print("============================================================")