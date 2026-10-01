import React from "react";

export interface BadgeProps {
  variant?: "success" | "warning" | "danger" | "info" | "default";
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ variant = "default", children, className = "" }) => {
  return <span className={`badge badge-${variant} px-2 py-1 rounded text-xs font-semibold ${className}`.trim()}>{children}</span>;
};

export default Badge;
