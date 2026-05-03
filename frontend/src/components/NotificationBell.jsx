import { Bell } from "lucide-react";
import { Button } from "@/components/ui/button";
import { formatBadgeCount } from "@/lib/alertas";
import { useNotifications } from "@/hooks/useNotifications";

function NotificationBell() {
  const { unreadCount } = useNotifications();
  const badgeValue = formatBadgeCount(unreadCount);

  return (
    <Button variant="ghost" size="icon" className="relative" data-testid="notifications-button" type="button">
      <Bell size={20} />
      {unreadCount > 0 && (
        <span className="absolute -top-1 -right-1 min-w-5 h-5 px-1 flex items-center justify-center rounded-full bg-red-500 text-white text-xs">
          {badgeValue}
        </span>
      )}
    </Button>
  );
}

export default NotificationBell;
