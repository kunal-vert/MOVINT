import type { ReactNode } from "react";

export interface DeploymentLayoutProps {
  children?: ReactNode;
}

export default function DeploymentLayout({ children }: DeploymentLayoutProps) {
  return <div>{children ?? "DeploymentLayout"}</div>;
}
