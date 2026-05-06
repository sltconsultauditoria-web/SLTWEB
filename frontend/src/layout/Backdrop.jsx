import { useSidebar } from "@/context/SidebarContext";

const Backdrop = () => {
  const { isMobileOpen, toggleMobileSidebar } = useSidebar();

  if (!isMobileOpen) {
    return null;
  }

  return (
    <button
      type="button"
      aria-label="Fechar navegação"
      className="fixed inset-0 z-30 bg-slate-950/50 backdrop-blur-sm md:hidden"
      onClick={toggleMobileSidebar}
    />
  );
};

export default Backdrop;
