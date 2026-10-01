import React from "react";
import Input from "../ui/Input";
import Select from "../ui/Select";

export interface TravelerFilterProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  statusFilter: string;
  onStatusChange: (value: string) => void;
}

export const TravelerFilter: React.FC<TravelerFilterProps> = ({
  searchTerm,
  onSearchChange,
  statusFilter,
  onStatusChange,
}) => {
  return (
    <div className="traveler-filter flex gap-4 items-center">
      <Input
        placeholder="Search passport or name..."
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
      />
      <Select
        value={statusFilter}
        onChange={(e) => onStatusChange(e.target.value)}
        options={[
          { label: "All Statuses", value: "ALL" },
          { label: "Active", value: "ACTIVE" },
          { label: "Completed", value: "COMPLETED" },
          { label: "Overdue", value: "OVERDUE" },
          { label: "Flagged", value: "FLAGGED" },
        ]}
      />
    </div>
  );
};

export default TravelerFilter;
