import React from "react";
import Badge from "../ui/Badge";

export interface TravelerItem {
  passport_id: string;
  full_name: string;
  nationality: string;
  current_journey_status?: string | null;
  current_risk_score?: number | null;
  watch_flag?: boolean;
}

export interface TravelerTableProps {
  travelers: TravelerItem[];
  onSelectTraveler?: (passportId: string) => void;
}

export const TravelerTable: React.FC<TravelerTableProps> = ({ travelers, onSelectTraveler }) => {
  return (
    <table className="traveler-table w-full border-collapse">
      <thead>
        <tr className="border-b text-left">
          <th className="p-2">Passport ID</th>
          <th className="p-2">Name</th>
          <th className="p-2">Nationality</th>
          <th className="p-2">Status</th>
          <th className="p-2">Risk Score</th>
        </tr>
      </thead>
      <tbody>
        {travelers.map((t) => (
          <tr
            key={t.passport_id}
            onClick={() => onSelectTraveler?.(t.passport_id)}
            className="border-b hover:bg-slate-50 cursor-pointer"
          >
            <td className="p-2">{t.passport_id}</td>
            <td className="p-2">{t.full_name}</td>
            <td className="p-2">{t.nationality}</td>
            <td className="p-2">
              {t.current_journey_status ? (
                <Badge variant={t.watch_flag ? "danger" : "info"}>{t.current_journey_status}</Badge>
              ) : (
                "-"
              )}
            </td>
            <td className="p-2">{t.current_risk_score ?? "N/A"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TravelerTable;
