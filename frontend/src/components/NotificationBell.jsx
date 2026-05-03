import { useEffect, useState } from "react";
import { Bell } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/context/AuthContext";
import { countBadgeAlertas, formatBadgeCount, normalizeAlertas } from "@/lib/alertas";

function NotificationBell() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let mounted = true;

    const carregarAlertas = async () => {
      try {
        const response = await api.get("/alertas/");
        if (!mounted) return;
        const items = normalizeAlertas(Array.isArray(response.data) ? response.data : []);
        setCount(countBadgeAlertas(items));
      } catch (error) {
        if (mounted) {
          setCount(0);
        }
      }
    };

    carregarAlertas();

    return () => {
      mounted = false;
    };
  }, []);

  const badgeValue = formatBadgeCount(count);

  return (
    <Button variant="ghost" size="icon" className="relative" data-testid="notifications-button" type="button">
      <Bell size={20} />
      {count > 0 && (
        <span className="absolute -top-1 -right-1 min-w-5 h-5 px-1 flex items-center justify-center rounded-full bg-red-500 text-white text-xs">
          {badgeValue}
        </span>
      )}
    </Button>
  );
}

export default NotificationBell;
