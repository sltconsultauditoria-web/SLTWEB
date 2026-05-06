import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const ErrorState = ({ title = "Erro ao carregar dados", description, onRetry, className }) => (
  <div className={cn("flex min-h-40 flex-col items-center justify-center gap-3 rounded-2xl border border-red-200 bg-red-50 p-8 text-center", className)}>
    <AlertCircle className="h-8 w-8 text-red-600" />
    <div>
      <p className="text-sm font-medium text-red-700">{title}</p>
      {description ? <p className="text-xs text-red-600">{description}</p> : null}
    </div>
    {onRetry ? (
      <Button type="button" variant="outline" onClick={onRetry}>
        Tentar novamente
      </Button>
    ) : null}
  </div>
);

export default ErrorState;
