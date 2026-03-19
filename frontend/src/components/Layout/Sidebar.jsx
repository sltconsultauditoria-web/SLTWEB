import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Building2, 
  FileText, 
  Calendar, 
  Bell, 
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Receipt,
  FileBarChart,
  Bot,
  Calculator,
  Shield,
  ScanLine
} from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { cn } from '@/lib/utils';

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
  { icon: Building2, label: 'Empresas', path: '/empresas' },
  { icon: FileText, label: 'Documentos', path: '/documentos' },
  { icon: Calendar, label: 'Obrigações', path: '/obrigacoes' },
  { icon: Receipt, label: 'DAS/Guias', path: '/guias' },
  { icon: Calculator, label: 'Fiscal (IRIS)', path: '/fiscal' },
  { icon: Shield, label: 'Auditoria', path: '/auditoria' },
  { icon: ScanLine, label: 'OCR', path: '/ocr' },
  { icon: Bot, label: 'Robôs', path: '/robos' },
  { icon: Bell, label: 'Alertas', path: '/alertas' },
  { icon: FileBarChart, label: 'Relatórios', path: '/relatorios' },
  { icon: Settings, label: 'Configurações', path: '/configuracoes' },
];

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const { logout, user } = useAuth();

  return (
    <aside 
      className={cn(
        "h-screen bg-blue-900 text-white flex flex-col transition-all duration-300",
        collapsed ? "w-16" : "w-64"
      )}
      data-testid="sidebar"
    >
      {/* Header */}
      <div className="p-4 border-b border-blue-800 flex items-center justify-between">
        {!collapsed && (
          <div>
            <h1 className="text-xl font-bold">SLTWEB</h1>
            <p className="text-xs text-blue-300">Gestão Fiscal</p>
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 hover:bg-blue-800 rounded"
          data-testid="toggle-sidebar"
        >
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      {/* Menu */}
      <nav className="flex-1 py-4">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "flex items-center px-4 py-3 transition-colors",
                isActive 
                  ? "bg-blue-800 border-r-4 border-white" 
                  : "hover:bg-blue-800/50",
                collapsed ? "justify-center" : "gap-3"
              )}
              data-testid={`menu-${item.label.toLowerCase()}`}
              title={collapsed ? item.label : undefined}
            >
              <Icon size={20} />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* User & Logout */}
      <div className="border-t border-blue-800 p-4">
        {!collapsed && user && (
          <div className="mb-3">
            <p className="text-sm font-medium truncate">{user.name || user.email}</p>
            <p className="text-xs text-blue-300 truncate">{user.email}</p>
          </div>
        )}
        <button
          onClick={logout}
          className={cn(
            "flex items-center text-red-300 hover:text-red-200 hover:bg-blue-800 rounded p-2 w-full transition-colors",
            collapsed ? "justify-center" : "gap-2"
          )}
          data-testid="logout-button"
          title={collapsed ? "Sair" : undefined}
        >
          <LogOut size={20} />
          {!collapsed && <span>Sair</span>}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
