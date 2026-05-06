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

import { Mail, Lock, Loader2 } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

const LoginPage = () => {
  const navigate = useNavigate();

  const { login, isAuthenticated, loading: authLoading } = useAuth();

  const [email, setEmail] = useState("admin@empresa.com");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const isSubmittingRef = useRef(false);

  // ======================================================
  // REDIRECIONAMENTO AUTOMÁTICO
  // ======================================================
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [authLoading, isAuthenticated, navigate]);

  // ======================================================
  // SUBMIT LOGIN
  // ======================================================
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (loading || isSubmittingRef.current) return;

    isSubmittingRef.current = true;
    setLoading(true);
    setError("");

    try {
      const result = await login(email.trim(), password);

      if (!result?.success) {
        throw new Error(
          result?.message || "Falha ao autenticar."
        );
      }

      // redireciona imediatamente
      navigate("/dashboard", { replace: true });
    } catch (err) {
      console.error("Erro no login:", err);

      setError(
        err?.message ||
          "Credenciais inválidas. Verifique email e senha."
      );
    } finally {
      setLoading(false);
      isSubmittingRef.current = false;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 px-4">
      <Card className="w-full max-w-md shadow-2xl rounded-2xl bg-white border-0">
        {/* HEADER */}
        <CardHeader className="text-center pt-8 pb-4">
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

        {/* CONTENT */}
        <CardContent className="px-8 pb-8">
          <form
            onSubmit={handleSubmit}
            className="space-y-5"
          >
            {/* EMAIL */}
            <div className="space-y-2">
              <Label
                htmlFor="email"
                className="text-gray-700 font-medium"
              >
                Email
              </Label>

              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />

                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  className="pl-10 h-12 rounded-lg"
                />
              </div>
            </div>

            {/* SENHA */}
            <div className="space-y-2">
              <Label
                htmlFor="password"
                className="text-gray-700 font-medium"
              >
                Senha
              </Label>

              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />

                <Input
                  id="password"
                  type="password"
                  placeholder="********"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  className="pl-10 h-12 rounded-lg"
                />
              </div>
            </div>

            {/* OPÇÕES */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Checkbox
                  id="remember"
                  checked={rememberMe}
                  onCheckedChange={(value) =>
                    setRememberMe(!!value)
                  }
                />

                <Label
                  htmlFor="remember"
                  className="text-sm text-gray-600 cursor-pointer font-normal"
                >
                  Permanecer logado
                </Label>
              </div>

              <button
                type="button"
                className="text-sm text-blue-600 hover:underline"
              >
                Esqueceu a senha?
              </button>
            </div>

            {/* ERRO */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-lg px-3 py-2 text-center">
                {error}
              </div>
            )}

            {/* BOTÃO */}
            <Button
              type="submit"
              disabled={loading || authLoading}
              className="w-full h-12 bg-blue-900 hover:bg-blue-800 text-white font-semibold rounded-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Entrando...
                </span>
              ) : (
                "Entrar"
              )}
            </Button>

            {/* DEBUG OPCIONAL */}
            <div className="text-center text-xs text-gray-400 pt-1">
              Ambiente conectado ao backend
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;
