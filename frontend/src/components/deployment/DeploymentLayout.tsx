import type { ReactNode } from "react";

export interface DeploymentLayoutProps {
  children?: ReactNode;
}

export default function DeploymentLayout({ children }: DeploymentLayoutProps) {
  return <div className="flex flex-1 flex-col">{children ?? "DeploymentLayout"}</div>;
}
