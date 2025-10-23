import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Crown } from "lucide-react";

interface UpgradeTooltipProps {
  children: React.ReactNode;
  feature: string;
  requiredPlan?: string;
  disabled?: boolean;
}

export function UpgradeTooltip({ 
  children, 
  feature, 
  requiredPlan = "Studio", 
  disabled = false 
}: UpgradeTooltipProps) {
  if (disabled) {
    return <>{children}</>;
  }

  return (
    <TooltipProvider>
      <Tooltip delayDuration={200}>
        <TooltipTrigger asChild>
          {children}
        </TooltipTrigger>
        <TooltipContent 
          side="top" 
          className="max-w-xs bg-gradient-to-r from-purple-600/95 to-pink-600/95 text-white border-purple-500/50 shadow-lg"
          data-testid="tooltip-upgrade"
        >
          <div className="flex items-start gap-2">
            <Crown className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <div className="flex flex-col gap-1">
              <p className="font-semibold text-sm">{feature}</p>
              <p className="text-xs text-purple-100">
                Upgrade to {requiredPlan} to unlock this feature
              </p>
            </div>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
