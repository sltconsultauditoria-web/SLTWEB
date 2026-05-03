import { useCallback, useEffect, useState } from "react";
import { Bell } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api } from "@/context/AuthContext";
import { countBadgeAlertas, formatBadgeCount, normalizeAlertas } from "@/lib/alertas";

function NotificationBell() {
  const [count, setCount] = useState(0);

  const carregarAlertas = useCallback(async () => {
    try {
      const response = await api.get("/alertas");
      const payload = response.data;
      const items = Array.isArray(payload)
        ? payload
        : Array.isArray(payload?.data)
          ? payload.data
          : Array.isArray(payload?.alertas)
            ? payload.alertas
            : [];

      setCount(countBadgeAlertas(normalizeAlertas(items)));
    } catch (error) {
      setCount(0);
    }
  }, []);

  useEffect(() => {
    let mounted = true;
    let intervalId = null;

    const run = async () => {
      if (!mounted) return;
      await carregarAlertas();
    };

    run();
    intervalId = window.setInterval(run, 30000);

    const handleVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        run();
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      mounted = false;
      if (intervalId) window.clearInterval(intervalId);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [carregarAlertas]);

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
