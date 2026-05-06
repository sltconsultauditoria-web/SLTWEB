import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import { isAdminUser } from "@/lib/rbac";
import LoginPage from "@/pages/LoginPage";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage";
import MainLayout from "@/components/Layout/MainLayout";
import Dashboard from "@/pages/Dashboard";
import Empresas from "@/pages/Empresas";
import Documentos from "@/pages/Documentos";
import Obrigacoes from "@/pages/Obrigacoes";
import CatalogoObrigacoes from "@/pages/CatalogoObrigacoes";
import Guias from "@/pages/Guias";
import Alertas from "@/pages/Alertas";
import Relatorios from "@/pages/Relatorios";
import Configuracoes from "@/pages/Configuracoes";
import ConfiguracoesUsuariosViewer from "@/pages/ConfiguracoesUsuariosViewer";
import ConfiguracaoAlertas from "@/pages/ConfiguracaoAlertas";
import Robos from "@/pages/Robos";
import Fiscal from "@/pages/Fiscal";
import Auditoria from "@/pages/Auditoria";
import OCR from "@/pages/OCR";
import TimelineEmpresa from "@/pages/TimelineEmpresa";
import Usuarios from "@/pages/Usuarios";

const AdminRoute = ({ children }) => {
  const { user } = useAuth();
  return isAdminUser(user) ? children : <Navigate to="/dashboard" replace />;
};

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter basename="/SLTWEB">
          <Routes>
            {/* Públicas */}
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/esqueci-senha" element={<ForgotPasswordPage />} />
            
            {/* Protegidas - Requer autenticação */}
            <Route element={<MainLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/empresas" element={<Empresas />} />
              <Route path="/empresas/:empresaId/timeline" element={<TimelineEmpresa />} />
              <Route path="/documentos" element={<Documentos />} />
              <Route path="/obrigacoes" element={<Obrigacoes />} />
              <Route path="/catalogo-obrigacoes" element={<CatalogoObrigacoes />} />
              <Route path="/guias" element={<Guias />} />
              <Route path="/alertas" element={<Alertas />} />
              <Route path="/relatorios" element={<Relatorios />} />
              <Route path="/configuracoes" element={<Configuracoes />} />
              <Route
                path="/configuracoes/usuarios-viewer"
                element={(
                  <AdminRoute>
                    <ConfiguracoesUsuariosViewer />
                  </AdminRoute>
                )}
              />
              <Route path="/config-alertas" element={<ConfiguracaoAlertas />} />
              <Route path="/robos" element={<Robos />} />
              <Route path="/fiscal" element={<Fiscal />} />
              <Route path="/auditoria" element={<Auditoria />} />
              <Route path="/ocr" element={<OCR />} />
              <Route
                path="/usuarios"
                element={(
                  <AdminRoute>
                    <Usuarios />
                  </AdminRoute>
                )}
              />
            </Route>
          </Routes>
        </BrowserRouter>
      </div>
    </AuthProvider>
  );
}

export default App;
