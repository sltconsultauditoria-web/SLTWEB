import { cn } from "@/lib/utils";

const FilterBar = ({ children, className }) => (
  <div className={cn("flex flex-wrap items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm", className)}>
    {children}
  </div>
);

export default FilterBar;
