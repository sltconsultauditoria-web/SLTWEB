/**
 * Componente de Login com Entra ID
 * Implementa fluxo OAuth com Entra ID (Azure AD)
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export function EntraIDLogin() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [user, setUser] = useState(null);

  // Processar callback do Entra ID
  useEffect(() => {
    const code = searchParams.get('code');
    const state = searchParams.get('state');

    if (code) {
      processCallback(code, state);
    }
  }, [searchParams]);

  const processCallback = async (code, state) => {
    setLoading(true);
    try {
      // Chamar endpoint de callback
      const response = await axios.get(`${API_URL}/api/auth/callback`, {
        params: { code, state }
      });

      const { access_token, refresh_token, user: userData } = response.data;

      // Armazenar tokens em localStorage (em produção, usar HttpOnly cookies)
      localStorage.setItem('access_token', access_token);
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token);
      }

      setUser(userData);
      setSuccess(true);

      // Redirecionar para dashboard após 2 segundos
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao processar autenticação');
      console.error('Erro no callback:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    setLoading(true);
    try {
      // Redirecionar para endpoint de login
      window.location.href = `${API_URL}/api/auth/login`;
    } catch (err) {
      setError('Erro ao iniciar login');
      setLoading(false);
    }
  };

  if (loading && !success) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Autenticando...</CardTitle>
            <CardDescription>Por favor, aguarde enquanto processamos sua autenticação</CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (success) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Autenticação Bem-Sucedida
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-gray-600">Bem-vindo,</p>
              <p className="font-semibold">{user?.displayName}</p>
              <p className="text-sm text-gray-600">{user?.mail}</p>
            </div>
            <p className="text-sm text-gray-600">Redirecionando para o dashboard...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="space-y-2">
          <CardTitle className="text-2xl">SLTWEB</CardTitle>
          <CardDescription>
            Faça login com sua conta Entra ID (Azure AD)
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-3">
            <Button
              onClick={handleLogin}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              size="lg"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Conectando...
                </>
              ) : (
                <>
                  <svg
                    className="mr-2 h-4 w-4"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M11.4 24H0V12.6h11.4V24zM24 24H12.6v-11.4H24V24zM11.4 12.6H0V1.2h11.4v11.4zm12.6 0H12.6V1.2H24v11.4z" />
                  </svg>
                  Fazer Login com Entra ID
                </>
              )}
            </Button>
          </div>

          <div className="text-center text-sm text-gray-600">
            <p>Você será redirecionado para fazer login com sua conta corporativa</p>
          </div>

          <div className="border-t pt-4">
            <p className="text-xs text-gray-500 text-center">
              Seguro e protegido por Entra ID (Azure AD)
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default EntraIDLogin;
