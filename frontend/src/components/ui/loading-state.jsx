import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

const LoadingState = ({ title = "Carregando", description, className }) => (
  <div className={cn("flex min-h-40 flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-slate-200 bg-white/60 p-8 text-center", className)}>
    <Loader2 className="h-6 w-6 animate-spin text-slate-500" />
    <div>
      <p className="text-sm font-medium text-slate-700">{title}</p>
      {description ? <p className="text-xs text-slate-500">{description}</p> : null}
    </div>
  </div>
);

export default LoadingState;
