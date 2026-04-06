import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { getAgentIcon, isAssetIcon } from "@/lib/agent-icons";

type IdentitySize = "xs" | "sm" | "default" | "lg";

export interface IdentityProps {
  name: string;
  avatarUrl?: string | null;
  icon?: string | null;
  initials?: string;
  size?: IdentitySize;
  className?: string;
}

function deriveInitials(name: string): string {
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
}

const textSize: Record<IdentitySize, string> = {
  xs: "text-sm",
  sm: "text-xs",
  default: "text-sm",
  lg: "text-sm",
};

export function Identity({ name, avatarUrl, icon, initials, size = "default", className }: IdentityProps) {
  const displayInitials = initials ?? deriveInitials(name);
  const assetUrl = isAssetIcon(icon) ? icon : null;
  const Icon = icon && !assetUrl ? getAgentIcon(icon) : null;

  return (
    <span className={cn("inline-flex gap-1.5", size === "xs" ? "items-baseline gap-1" : "items-center", size === "lg" && "gap-2", className)}>
      <Avatar size={size} className={size === "xs" ? "relative -top-px" : undefined}>
        {(avatarUrl || assetUrl) && <AvatarImage src={(avatarUrl || assetUrl)!} alt={name} />}
        <AvatarFallback>
          {Icon && !avatarUrl && !assetUrl ? <Icon className={cn("h-3.5 w-3.5", size === "lg" && "h-4 w-4", size === "xs" && "h-3 w-3")} /> : displayInitials}
        </AvatarFallback>
      </Avatar>
      <span className={cn("truncate", textSize[size])}>{name}</span>
    </span>
  );
}
