import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { isAdminUser } from "@/lib/rbac";
import { useAuth } from "@/context/AuthContext";

const SidebarWidget = ({ collapsed = false, mobile = false }) => {
  const { user } = useAuth();
  const isAdmin = isAdminUser(user);

  return (
    <div className={cn("rounded-xl border border-white/10 bg-white/5 px-3 py-3", collapsed && !mobile && "px-2")}>
      <p className={cn("text-xs uppercase tracking-[0.18em] text-slate-400", collapsed && !mobile && "sr-only")}>
        Sessão
      </p>
      <div className={cn("mt-2 flex items-center gap-3", collapsed && !mobile && "justify-center")}>
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
  );
};

export default SidebarWidget;
