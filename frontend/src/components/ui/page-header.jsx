import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const PageHeader = ({
  title,
  description,
  actions,
  badge,
  className,
}) => {
  return (
    <div className={cn("flex flex-col gap-4 md:flex-row md:items-end md:justify-between", className)}>
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900 md:text-3xl">{title}</h1>
          {badge ? <Badge variant={badge.variant || "outline"}>{badge.label}</Badge> : null}
        </div>
        {description ? <p className="mt-1 max-w-3xl text-sm text-slate-500">{description}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap gap-2">{actions}</div> : null}
    </div>
  );
};

export default PageHeader;
