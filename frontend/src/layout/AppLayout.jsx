import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { SidebarProvider } from "@/context/SidebarContext";
import AppHeader from "./AppHeader";
import AppSidebar from "./AppSidebar";
import Backdrop from "./Backdrop";

const LayoutFrame = () => {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <AppSidebar />
      <Backdrop />

      <div className="flex min-w-0 flex-1 flex-col">
        <AppHeader />
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <div className="mx-auto flex w-full max-w-[1600px] flex-col gap-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

const AppLayout = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-slate-900" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <SidebarProvider>
      <LayoutFrame />
    </SidebarProvider>
  );
};

export default AppLayout;
