import { createContext, useContext, useEffect, useMemo, useState } from "react";

const SidebarContext = createContext(undefined);

export const useSidebar = () => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return context;
};

export const SidebarProvider = ({ children }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);

      if (!mobile) {
        setIsMobileOpen(false);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const value = useMemo(
    () => ({
      isExpanded,
      isMobileOpen,
      isHovered,
      isMobile,
      toggleSidebar: () => setIsExpanded((prev) => !prev),
      toggleMobileSidebar: () => setIsMobileOpen((prev) => !prev),
      setIsHovered,
    }),
    [isExpanded, isMobileOpen, isHovered, isMobile]
  );

  return <SidebarContext.Provider value={value}>{children}</SidebarContext.Provider>;
};
