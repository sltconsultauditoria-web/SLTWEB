import { cn } from "@/lib/utils";

const EmptyState = ({ title = "Nenhum registro encontrado", description, icon: Icon, action, className }) => (
  <div className={cn("flex min-h-40 flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-slate-200 bg-white/60 p-8 text-center", className)}>
    {Icon ? <Icon className="h-8 w-8 text-slate-300" /> : null}
    <div>
      <p className="text-sm font-medium text-slate-700">{title}</p>
      {description ? <p className="text-xs text-slate-500">{description}</p> : null}
    </div>
    {action ? <div className="pt-1">{action}</div> : null}
  </div>
);

export default EmptyState;
