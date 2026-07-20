import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "danger" | "ghost";
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  icon?: ReactNode;
  children?: ReactNode;
}

const variantClasses: Record<Variant, string> = {
  primary:
    "bg-navy-700 text-white hover:bg-navy-800 focus-visible:ring-navy-400",
  secondary:
    "bg-neutral-100 text-navy-700 hover:bg-neutral-200 focus-visible:ring-navy-300",
  danger:
    "bg-white text-status-offline border border-netural-200 hover:bg-red-50 focus-visible:ring-status-offline",
  ghost:
    "bg-transparent text-navy-700 hover:bg-navy-50 focus-visible:ring-navy-300",
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
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${variantClasses[variant]} ${className}`}
      {...rest}
    >
      {icon}
      {children}
    </button>
  );
}
