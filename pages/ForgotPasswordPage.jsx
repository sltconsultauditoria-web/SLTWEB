import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Mail, ArrowLeft, CheckCircle } from "lucide-react";
import { Link } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await axios.post(`${API}/auth/forgot-password`, { email });
      setSuccess(true);
    } catch (err) {
      console.error("Forgot password error:", err);
      setError("Erro ao enviar email de recuperação. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600" data-testid="forgot-password-page">
        <Card className="w-full max-w-md mx-4 shadow-2xl rounded-2xl bg-white" data-testid="forgot-password-card">
          <CardHeader className="text-center pb-2 pt-8">
            <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
            <CardTitle className="text-2xl font-bold text-blue-900" data-testid="success-title">
              Email Enviado!
            </CardTitle>
            <CardDescription className="text-gray-600 mt-2" data-testid="success-description">
              Verifique sua caixa de entrada para redefinir sua senha.
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6 px-8 pb-8">
            <Link to="/login">
              <Button
                className="w-full h-12 bg-blue-900 hover:bg-blue-800 text-white font-semibold rounded-lg transition-colors"
                data-testid="back-to-login-button"
              >
                <ArrowLeft className="mr-2 h-5 w-5" />
                Voltar para Login
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600" data-testid="forgot-password-page">
      <Card className="w-full max-w-md mx-4 shadow-2xl rounded-2xl bg-white" data-testid="forgot-password-card">
        <CardHeader className="text-center pb-2 pt-8">
          <CardTitle className="text-3xl font-bold text-blue-900" data-testid="forgot-password-title">
            SLTWEB
          </CardTitle>
          <CardDescription className="text-gray-600 mt-2" data-testid="forgot-password-subtitle">
            Recuperação de Senha
          </CardDescription>
          <p className="text-sm text-gray-500 mt-1">
            Powered by SLT Consult
          </p>
        </CardHeader>
        <CardContent className="pt-6 px-8 pb-8">
          <p className="text-sm text-gray-600 mb-6 text-center" data-testid="forgot-password-instruction">
            Digite seu email para receber as instruções de recuperação de senha.
          </p>
          <form onSubmit={handleSubmit} className="space-y-5" data-testid="forgot-password-form">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-700 font-medium" data-testid="email-label">
                Email
              </Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10 h-12 rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                  data-testid="email-input"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="text-red-500 text-sm text-center" data-testid="forgot-password-error">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full h-12 bg-blue-900 hover:bg-blue-800 text-white font-semibold rounded-lg transition-colors"
              disabled={loading}
              data-testid="forgot-password-submit-button"
            >
              {loading ? "Enviando..." : "Enviar Email de Recuperação"}
            </Button>

            <div className="text-center">
              <Link
                to="/login"
                className="text-sm text-blue-600 hover:text-blue-800 hover:underline inline-flex items-center"
                data-testid="back-to-login-link"
              >
                <ArrowLeft className="mr-1 h-4 w-4" />
                Voltar para Login
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default ForgotPasswordPage;
