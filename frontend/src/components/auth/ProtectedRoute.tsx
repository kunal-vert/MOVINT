import type { ReactNode } from "react";

export interface ProtectedRouteProps {
  children?: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  return <div>{children ?? "ProtectedRoute"}</div>;
}
