import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";

import { Mail, Lock } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { login, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  // 🔒 Proteção contra múltiplos submits (React 18 / double render)
  const isSubmittingRef = useRef(false);

  /**
   * ✅ Redirecionamento seguro
   * Só navega quando:
   * - autenticação já terminou
   * - usuário está autenticado
   */
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [authLoading, isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // 🛑 Evita login duplicado
    if (isSubmittingRef.current || loading) return;

    isSubmittingRef.current = true;
    setLoading(true);
    setError("");

    try {
      await login(email.trim(), password);
      // redirecionamento acontece no useEffect
    } catch (err) {
      console.error("Erro no login:", err);
      setError("Credenciais inválidas. Verifique email e senha.");
    } finally {
      setLoading(false);
      isSubmittingRef.current = false;
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600"
      data-testid="login-page"
    >
      <Card className="w-full max-w-md mx-4 shadow-2xl rounded-2xl bg-white">
        <CardHeader className="text-center pb-2 pt-8">
          <CardTitle className="text-3xl font-bold text-blue-900">
            SLTWEB
          </CardTitle>
          <CardDescription className="text-gray-600 mt-2">
            Sistema de Gestão Fiscal Integrada
          </CardDescription>
          <p className="text-sm text-gray-500 mt-1">
            Powered by SLT Consult
          </p>
        </CardHeader>

        <CardContent className="pt-6 px-8 pb-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* EMAIL */}
            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-700 font-medium">
                Email
              </Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10 h-12 rounded-lg"
                  required
                  autoComplete="email"
                />
              </div>
            </div>

            {/* SENHA */}
            <div className="space-y-2">
              <Label htmlFor="password" className="text-gray-700 font-medium">
                Senha
              </Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  id="password"
                  type="password"
                  placeholder="********"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 h-12 rounded-lg"
                  required
                  autoComplete="current-password"
                />
              </div>
            </div>

            {/* OPÇÕES */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="remember"
                  checked={rememberMe}
                  onCheckedChange={setRememberMe}
                />
                <Label
                  htmlFor="remember"
                  className="text-sm text-gray-600 cursor-pointer font-normal"
                >
                  Permanecer logado
                </Label>
              </div>

              <a
                href="/esqueci-senha"
                className="text-sm text-blue-600 hover:underline"
              >
                Esqueceu a senha?
              </a>
            </div>

            {/* ERRO */}
            {error && (
              <div className="text-red-500 text-sm text-center">
                {error}
              </div>
            )}

            {/* BOTÃO */}
            <Button
              type="submit"
              disabled={loading || authLoading}
              className="w-full h-12 bg-blue-900 hover:bg-blue-800 text-white font-semibold rounded-lg"
            >
              {loading ? "Entrando..." : "Entrar"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;
