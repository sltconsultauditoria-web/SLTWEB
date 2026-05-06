import { useCallback, useMemo } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { ChevronLeft, ChevronRight, LogOut, Shield, Building2 } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useSidebar } from "@/context/SidebarContext";
import { cn } from "@/lib/utils";
import { isAdminUser } from "@/lib/rbac";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { navigationGroups } from "@/components/Layout/navigation";
import SidebarWidget from "./SidebarWidget";

const iconFallback = (label) => {
  if (label === "Empresas") return Building2;
  return Shield;
};

const SidebarLink = ({ item, collapsed, mobile = false, onNavigate }) => {
  const Icon = item.icon || iconFallback(item.label);

  return (
    <NavLink
      to={item.path}
      onClick={onNavigate}
      title={collapsed && !mobile ? item.label : undefined}
      data-testid={`menu-${item.label.toLowerCase().replace(/\s+/g, "-")}`}
      className={({ isActive }) =>
        cn(
          "group flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150",
          isActive
            ? "bg-primary text-primary-foreground shadow-sm"
            : "text-slate-200 hover:bg-white/10 hover:text-white",
          collapsed && !mobile ? "justify-center px-2" : "gap-3"
        )
      }
    >
      <Icon size={18} className="shrink-0" />
      {(!collapsed || mobile) && <span className="truncate">{item.label}</span>}
    </NavLink>
  );
};

export const SidebarNav = ({ mobile = false, onNavigate }) => {
  const { isExpanded, isHovered, setIsHovered, toggleSidebar, toggleMobileSidebar, isMobileOpen } = useSidebar();
  const { user, logout } = useAuth();
  const isAdmin = isAdminUser(user);
  const location = useLocation();

  const collapsed = !mobile && !isExpanded && !isHovered;

  const onClickLogout = useCallback(() => logout(), [logout]);

  const groups = useMemo(
    () =>
      navigationGroups.map((group) => ({
        ...group,
        items: group.items.filter((item) => !item.adminOnly || isAdmin),
      })),
    [isAdmin]
  );

  return (
    <div className={cn("flex h-full flex-col", mobile ? "bg-slate-950 text-white" : "bg-slate-950 text-white")}>
      <div className="flex items-start justify-between gap-3 px-4 pb-4 pt-4">
        <div className={cn("min-w-0", collapsed && "sr-only")}>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-slate-400">SLTWEB</p>
          <h1 className="mt-1 text-lg font-semibold text-white">Enterprise Fiscal Hub</h1>
          <p className="text-xs text-slate-400">Painel operacional e administrativo</p>
        </div>

        {!mobile && (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={toggleSidebar}
            className="h-8 w-8 text-slate-300 hover:bg-white/10 hover:text-white"
            data-testid="toggle-sidebar"
            title={collapsed ? "Expandir" : "Recolher"}
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </Button>
        )}
      </div>

      <div className="px-4 pb-4">
        <SidebarWidget collapsed={collapsed} mobile={mobile} />
      </div>

      <div className="mx-4 h-px bg-white/10" />

      <div className="flex-1 overflow-y-auto px-3 py-4">
        <div className="space-y-6">
          {groups.map((group) => (
            <div key={group.title}>
              <div className={cn("px-3 pb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400", collapsed && "sr-only")}>
                {group.title}
              </div>
              <div className="space-y-1">
                {group.items.map((item) => (
                  <SidebarLink
                    key={item.path}
                    item={item}
                    collapsed={collapsed}
                    mobile={mobile}
                    onNavigate={() => {
                      if (mobile) {
                        toggleMobileSidebar();
                      }

                      if (onNavigate) {
                        onNavigate();
                      }
                    }}
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
          onClick={onClickLogout}
          className={cn(
            "w-full justify-start gap-3 rounded-lg text-red-300 hover:bg-red-500/10 hover:text-red-200",
            collapsed && !mobile && "justify-center px-2"
          )}
          data-testid="logout-button"
          title={collapsed && !mobile ? "Sair" : undefined}
        >
          <LogOut className="h-4 w-4" />
          {!collapsed && <span>Sair</span>}
        </Button>
      </div>
    </div>
  );
};

const AppSidebar = () => {
  const { isExpanded, isHovered, isMobileOpen, setIsHovered } = useSidebar();

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 h-screen shrink-0 transform border-r border-slate-800 bg-slate-950 text-white shadow-2xl shadow-slate-950/30 transition-all duration-300 ease-in-out md:sticky md:top-0 md:z-20 md:translate-x-0",
        isMobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0",
        isExpanded || isHovered ? "md:w-72" : "md:w-20",
        "w-72"
      )}
      onMouseEnter={() => {
        if (!isMobileOpen && !isExpanded) {
          setIsHovered(true);
        }
      }}
      onMouseLeave={() => setIsHovered(false)}
      data-testid="sidebar"
    >
      <SidebarNav />
    </aside>
  );
};

export default AppSidebar;
