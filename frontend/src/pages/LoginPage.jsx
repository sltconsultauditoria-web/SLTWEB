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
  const [email, setEmail] = useState("admin@empresa.com");
  const [password, setPassword] = useState("admin123");

  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { login, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const isSubmittingRef = useRef(false);

  // redirect seguro
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [authLoading, isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isSubmittingRef.current) return;

    isSubmittingRef.current = true;
    setLoading(true);
    setError("");

    try {
      await login(email.trim(), password);
    } catch (err) {
      const msg =
        err?.response?.status === 404
          ? "Endpoint /auth/login não encontrado (backend não carregou auth router)"
          : "Credenciais inválidas ou erro no servidor";

      setError(msg);
    } finally {
      setLoading(false);
      isSubmittingRef.current = false;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600">
      <Card className="w-full max-w-md mx-4 shadow-2xl rounded-2xl bg-white">
        <CardHeader className="text-center pt-8">
          <CardTitle className="text-3xl font-bold text-blue-900">
            SLTWEB
          </CardTitle>
          <CardDescription className="text-gray-600">
            Sistema de Gestão Fiscal Integrada
          </CardDescription>
        </CardHeader>

        <CardContent className="px-8 pb-8 pt-6">
          <form onSubmit={handleSubmit} className="space-y-5">

            {/* EMAIL */}
            <div>
              <Label>Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-gray-400" />
                <Input
                  className="pl-10"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                />
              </div>
            </div>

            {/* PASSWORD */}
            <div>
              <Label>Senha</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" />
                <Input
                  className="pl-10"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  type="password"
                  required
                />
              </div>
            </div>

            {/* OPTIONS */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Checkbox
                  checked={rememberMe}
                  onCheckedChange={setRememberMe}
                />
                <span className="text-sm">Lembrar</span>
              </div>

              <a className="text-sm text-blue-600" href="/forgot">
                Esqueci senha
              </a>
            </div>

            {/* ERROR */}
            {error && (
              <div className="text-red-500 text-sm">{error}</div>
            )}

            {/* BUTTON */}
            <Button
              type="submit"
              disabled={loading || authLoading}
              className="w-full"
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