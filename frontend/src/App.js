import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "@/context/AuthContext";

import LoginPage from "@/pages/LoginPage";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage";

import MainLayout from "@/components/Layout/MainLayout";

import Dashboard from "@/pages/Dashboard";
import Empresas from "@/pages/Empresas";
import Documentos from "@/pages/Documentos";
import Obrigacoes from "@/pages/Obrigacoes";
import Guias from "@/pages/Guias";
import Alertas from "@/pages/Alertas";
import Relatorios from "@/pages/Relatorios";
import Configuracoes from "@/pages/Configuracoes";
import ConfiguracaoAlertas from "@/pages/ConfiguracaoAlertas";
import Robos from "@/pages/Robos";
import Fiscal from "@/pages/Fiscal";
import Auditoria from "@/pages/Auditoria";
import OCR from "@/pages/OCR";

// 🔐 Componente para proteger rotas
function PrivateRoute({ children }) {
  const { token } = useAuth();

  return token ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter basename="/SLTWEB">
        <div className="App">
          <Routes>

            {/* Redirecionamento inicial */}
            <Route path="/" element={<Navigate to="/login" replace />} />

            {/* Públicas */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/esqueci-senha" element={<ForgotPasswordPage />} />

            {/* Privadas */}
            <Route
              element={
                <PrivateRoute>
                  <MainLayout />
                </PrivateRoute>
              }
            >
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/empresas" element={<Empresas />} />
              <Route path="/documentos" element={<Documentos />} />
              <Route path="/obrigacoes" element={<Obrigacoes />} />
              <Route path="/guias" element={<Guias />} />
              <Route path="/alertas" element={<Alertas />} />
              <Route path="/relatorios" element={<Relatorios />} />
              <Route path="/configuracoes" element={<Configuracoes />} />
              <Route path="/config-alertas" element={<ConfiguracaoAlertas />} />
              <Route path="/robos" element={<Robos />} />
              <Route path="/fiscal" element={<Fiscal />} />
              <Route path="/auditoria" element={<Auditoria />} />
              <Route path="/ocr" element={<OCR />} />
            </Route>

          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;