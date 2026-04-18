import { useState } from "react";
import api from "../services/api";

export default function LoginPage() {
  const [email, setEmail] = useState(""); // ✅ corrigido
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await api.post("/login", {
        email,          // ✅ backend espera email
        password
      });

      // ✅ padrão do seu backend
      const data = res.data?.data;

      if (!data?.token) {
        throw new Error("Token não recebido");
      }

      // 💾 salvar sessão
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      // 🔄 redirecionar (ajuste rota se necessário)
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
    <div style={{ maxWidth: 400, margin: "auto", marginTop: 100 }}>
      <h1>Login</h1>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 10 }}
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 10 }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{ width: "100%" }}
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>

      {error && (
        <p style={{ color: "red", marginTop: 10 }}>
          {error}
        </p>
      )}
    </div>
  );
}