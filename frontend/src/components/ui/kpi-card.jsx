import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

const KPICard = ({ title, value, icon: Icon, tone = "slate", subtitle, trend, className, loading = false, ...props }) => {
  const toneStyles = {
    slate: "bg-slate-900 text-white",
    blue: "bg-blue-600 text-white",
    emerald: "bg-emerald-600 text-white",
    amber: "bg-amber-500 text-white",
    rose: "bg-rose-600 text-white",
    violet: "bg-violet-600 text-white",
    cyan: "bg-cyan-600 text-white",
  };

  return (
    <Card className={cn("border-slate-200 shadow-sm", className)} {...props}>
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-sm font-medium text-slate-500">{title}</p>
            {loading ? (
              <div className="mt-2 h-8 w-28 animate-pulse rounded-md bg-slate-200" />
            ) : (
              <p className="mt-1 text-3xl font-semibold tracking-tight text-slate-900">{value}</p>
            )}
            {subtitle ? <p className="mt-1 text-xs text-slate-400">{subtitle}</p> : null}
            {trend ? <p className="mt-2 text-xs font-medium text-slate-500">{trend}</p> : null}
          </div>
          {Icon ? (
            <div className={cn("flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl", toneStyles[tone] || toneStyles.slate)}>
              <Icon className="h-5 w-5" />
            </div>
          ) : null}
        </div>
      </CardContent>
    </Card>
  );
};

export default KPICard;
