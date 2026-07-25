import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "danger" | "ghost";
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  icon?: ReactNode;
  children?: ReactNode;
}

const variantClasses: Record<Variant, string> = {
  primary:
    "bg-primary text-text-inverse hover:bg-secondary-hover focus-visible:ring-focus disabled:bg-disabled disabled:text-disabled-text",
  secondary:
    "bg-surface text-primary hover:bg-surface-2 focus-visible:ring-focus disabled:bg-disabled disabled:text-disabled-text",
  danger:
    "bg-surface text-danger border border-border hover:bg-danger/10 focus-visible:ring-danger disabled:bg-disabled disabled:text-disabled-text",
  ghost:
    "bg-ghost text-primary hover:bg-surface-2 focus-visible:ring-focus disabled:bg-disabled disabled:text-disabled-text",
};
export function Button({
  variant = "primary",
  icon,
  children,
  className = "",
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors duration-150 [&>svg]:size-5 [&>svg]:shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${variantClasses[variant]} ${className}`}
      {...rest}
    >
      {icon}
      {children}
    </button>
  );
}
