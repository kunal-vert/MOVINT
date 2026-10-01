export type JourneyStatus = "ACTIVE" | "COMPLETED" | "OVERDUE" | "FLAGGED";

export interface ComponentBaseProps {
  className?: string;
  children?: React.ReactNode;
}
