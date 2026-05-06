import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const statusMap = {
  success: "bg-emerald-600 text-white hover:bg-emerald-600",
  warning: "bg-amber-500 text-white hover:bg-amber-500",
  danger: "bg-rose-600 text-white hover:bg-rose-600",
  pending: "bg-slate-500 text-white hover:bg-slate-500",
  processing: "bg-blue-600 text-white hover:bg-blue-600",
  active: "bg-emerald-600 text-white hover:bg-emerald-600",
  inactive: "bg-slate-400 text-white hover:bg-slate-400",
};

const StatusBadge = ({ status, label, className }) => {
  const key = String(status || "").toLowerCase();
  const tone = statusMap[key] || "bg-slate-600 text-white hover:bg-slate-600";
  return (
    <Badge className={cn("rounded-full px-2.5 py-0.5 text-xs font-semibold", tone, className)}>
      {label || status || "status"}
    </Badge>
  );
};

export default StatusBadge;
