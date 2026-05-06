import { cn } from "@/lib/utils";

const EntityForm = ({ children, className, ...props }) => (
  <form className={cn("space-y-4", className)} {...props}>
    {children}
  </form>
);

export default EntityForm;
