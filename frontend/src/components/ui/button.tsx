import * as React from "react";
import { cn } from "../../lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "destructive" | "ghost";
  size?: "default" | "sm";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant="default", size="default", ...props }, ref) => {
    const base = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black disabled:opacity-50 disabled:pointer-events-none";
    const variants: Record<string,string> = {
      default: "bg-black text-white hover:bg-black/90",
      outline: "border border-black/20 hover:bg-black/5",
      destructive: "bg-red-600 text-white hover:bg-red-600/90",
      ghost: "hover:bg-black/5"
    };
    const sizes: Record<string,string> = { default: "h-9 px-3", sm: "h-8 px-2" };
    return (
      <button ref={ref} className={cn(base, variants[variant], sizes[size], className)} {...props} />
    );
  }
);
Button.displayName = "Button";
