import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export function EntraIDLogin() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="space-y-2">
          <CardTitle className="text-2xl">SLTWEB</CardTitle>
          <CardDescription>
            Fluxo legado desativado para evitar URLs manuais em producao.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Este componente foi neutralizado. O login oficial usa o fluxo principal da aplicacao.
            </AlertDescription>
          </Alert>

          <div className="border-t pt-4">
            <p className="text-xs text-gray-500 text-center">
              Nao utiliza URL manual de login.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default EntraIDLogin;
