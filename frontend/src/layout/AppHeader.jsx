import { useLocation } from "react-router-dom";
import { Menu, Search } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useSidebar } from "@/context/SidebarContext";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import NotificationBell from "@/components/NotificationBell";
import { cn } from "@/lib/utils";
import { isAdminUser } from "@/lib/rbac";
import { resolveRouteTitle } from "@/components/Layout/navigation";

const AppHeader = () => {
  const location = useLocation();
  const { user } = useAuth();
  const { title, description } = resolveRouteTitle(location.pathname);
  const { isMobileOpen, toggleSidebar, toggleMobileSidebar } = useSidebar();
  const isAdmin = isAdminUser(user);

  const handleToggle = () => {
    if (window.innerWidth >= 768) {
      toggleSidebar();
      return;
    }

    toggleMobileSidebar();
  };

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/70 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/75">
      <div className="flex min-h-20 items-center gap-4 px-4 py-3 md:px-6">
        <div className="flex items-center gap-3 md:hidden">
          <Button variant="outline" size="icon" className="h-10 w-10" type="button" onClick={handleToggle}>
            <Menu className="h-5 w-5" />
            <span className="sr-only">{isMobileOpen ? "Fechar navegação" : "Abrir navegação"}</span>
          </Button>
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2 text-xs font-medium uppercase tracking-[0.2em] text-slate-500">
            <span>SLTWEB</span>
            <span className="text-slate-300">/</span>
            <span>{title}</span>
          </div>
          <div className="mt-1 flex items-start gap-3">
            <div className="min-w-0">
              <h2 className="truncate text-xl font-semibold text-slate-900 md:text-2xl">{title}</h2>
              <p className="truncate text-sm text-slate-500">{description}</p>
            </div>
            <Badge
              variant={isAdmin ? "default" : "secondary"}
              className={cn("hidden rounded-full md:inline-flex", isAdmin && "bg-rose-600 text-white hover:bg-rose-600")}
            >
              {isAdmin ? "ADMIN" : "VIEWER"}
            </Badge>
          </div>
        </div>

        <div className="hidden min-w-[18rem] max-w-[28rem] flex-1 lg:block">
          <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-slate-500">
            <Search className="h-4 w-4 shrink-0" />
            <span className="truncate text-sm">Painel operacional e fiscal</span>
          </div>
        </div>

        <div className="ml-auto flex items-center gap-3">
          <NotificationBell />
          <div className="hidden items-center gap-3 rounded-2xl border border-slate-200 bg-white px-3 py-2 shadow-sm sm:flex">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">
              {user?.name?.charAt(0) || user?.email?.charAt(0) || "U"}
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-slate-900">{user?.name || "Usuário"}</p>
              <p className="truncate text-xs text-slate-500">{user?.email}</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AppHeader;
