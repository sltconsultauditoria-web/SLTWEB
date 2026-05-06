import { NavLink } from "react-router-dom";
import {
  ChevronLeft,
  ChevronRight,
  LogOut,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { isAdminUser } from "@/lib/rbac";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { navigationGroups } from "./navigation";

export const menuItems = [
  { icon: null, label: "Dashboard", path: "/dashboard" },
  { icon: null, label: "Empresas", path: "/empresas" },
  { icon: null, label: "Documentos", path: "/documentos" },
  { icon: null, label: "Obrigações", path: "/obrigacoes" },
  { icon: null, label: "Catálogo Fiscal", path: "/catalogo-obrigacoes" },
  { icon: null, label: "DAS/Guias", path: "/guias" },
  { icon: null, label: "Fiscal (IRIS)", path: "/fiscal" },
  { icon: null, label: "Auditoria", path: "/auditoria" },
  { icon: null, label: "OCR", path: "/ocr" },
  { icon: null, label: "Robôs", path: "/robos" },
  { icon: null, label: "Alertas", path: "/alertas" },
  { icon: null, label: "Relatórios", path: "/relatorios" },
  { icon: null, label: "Usuários", path: "/usuarios", adminOnly: true },
  { icon: null, label: "Configurações", path: "/configuracoes" },
  { icon: null, label: "Viewers", path: '/configuracoes/usuarios-viewer', adminOnly: true },
];

const SidebarLink = ({ item, collapsed, onNavigate }) => {
  const Icon = item.icon;

  return (
    <NavLink
      to={item.path}
      onClick={onNavigate}
      className={({ isActive }) =>
        cn(
          "group flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150",
          isActive
            ? "bg-primary text-primary-foreground shadow-sm"
            : "text-slate-200 hover:bg-white/10 hover:text-white",
          collapsed ? "justify-center px-2" : "gap-3"
        )
      }
      title={collapsed ? item.label : undefined}
      data-testid={`menu-${item.label.toLowerCase()}`}
    >
      {Icon ? <Icon size={18} className="shrink-0" /> : <span className="h-4 w-4 shrink-0 rounded-full bg-current/60" />}
      {!collapsed && <span className="truncate">{item.label}</span>}
    </NavLink>
  );
};

export const SidebarNav = ({
  collapsed = false,
  onNavigate,
  onToggleCollapsed,
  mobile = false,
}) => {
  const { user, logout } = useAuth();
  const isAdmin = isAdminUser(user);

  return (
    <div className={cn("flex h-full flex-col", mobile && "bg-slate-950 text-white")}>
      <div className="flex items-start justify-between gap-3 px-4 pb-4 pt-4">
        <div className={cn("min-w-0", collapsed && !mobile && "sr-only")}>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-400">
            SLTWEB
          </p>
          <h1 className="mt-1 text-lg font-semibold text-white">Enterprise Fiscal Hub</h1>
          <p className="text-xs text-slate-400">Painel operacional e administrativo</p>
        </div>
        {!mobile && (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={onToggleCollapsed}
            className="h-8 w-8 text-slate-300 hover:bg-white/10 hover:text-white"
            data-testid="toggle-sidebar"
            title={collapsed ? "Expandir" : "Recolher"}
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>
        )}
      </div>

      <div className="px-4 pb-4">
        <div className="rounded-xl border border-white/10 bg-white/5 px-3 py-3">
          <p className="text-xs uppercase tracking-[0.18em] text-slate-400">Sessão</p>
          <div className="mt-2 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
              {user?.name?.charAt(0) || user?.email?.charAt(0) || "U"}
            </div>
            <div className={cn("min-w-0", collapsed && !mobile && "hidden")}>
              <p className="truncate text-sm font-semibold text-white">{user?.name || "Usuário"}</p>
              <p className="truncate text-xs text-slate-400">{user?.email}</p>
            </div>
          </div>
          <div className={cn("mt-3 flex flex-wrap gap-2", collapsed && !mobile && "hidden")}>
            <Badge variant={isAdmin ? "default" : "secondary"} className="rounded-full">
              {isAdmin ? "ADMIN" : "VIEWER"}
            </Badge>
            <Badge variant="outline" className="border-white/15 text-slate-200">
              {user?.role || user?.perfil || "user"}
            </Badge>
          </div>
        </div>
      </div>

      <div className="mx-4 h-px bg-white/10" />

      <div className="flex-1 overflow-y-auto px-3 py-4">
        <div className="space-y-6">
          {navigationGroups.map((group) => (
            <div key={group.title}>
              <div className={cn("px-3 pb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400", collapsed && !mobile && "sr-only")}>
                {group.title}
              </div>
              <div className="space-y-1">
                {group.items
                  .filter((item) => !item.adminOnly || isAdmin)
                  .map((item) => (
                    <SidebarLink
                      key={item.path}
                      item={item}
                      collapsed={collapsed}
                      onNavigate={onNavigate}
                    />
                  ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="border-t border-white/10 p-4">
        <Button
          type="button"
          variant="ghost"
          onClick={logout}
          className={cn(
            "w-full justify-start gap-3 rounded-lg text-red-300 hover:bg-red-500/10 hover:text-red-200",
            collapsed && !mobile && "justify-center px-2"
          )}
          data-testid="logout-button"
          title={collapsed ? "Sair" : undefined}
        >
          <LogOut className="h-4 w-4" />
          {!collapsed && <span>Sair</span>}
        </Button>
      </div>
    </div>
  );
};

const Sidebar = ({ collapsed, setCollapsed }) => {
  return (
    <aside
      className={cn(
        "hidden h-screen shrink-0 border-r border-slate-800 bg-slate-950 text-white shadow-2xl shadow-slate-950/30 md:flex md:flex-col",
        collapsed ? "w-20" : "w-72"
      )}
      data-testid="sidebar"
    >
      <SidebarNav
        collapsed={collapsed}
        onToggleCollapsed={() => setCollapsed((value) => !value)}
      />
    </aside>
  );
};

Sidebar.displayName = "Sidebar";

export default Sidebar;
