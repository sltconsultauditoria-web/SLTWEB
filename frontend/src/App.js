import "@/App.css";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";

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

function App() {
  return (
    <AuthProvider>
      <div className="App">

          <Routes>

            <Route path="/" element={<Navigate to="/login" replace />} />

            <Route path="/login" element={<LoginPage />} />

            <Route path="/esqueci-senha" element={<ForgotPasswordPage />} />

            <Route element={<MainLayout />}>

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
    </AuthProvider>
  );
}

export default App;