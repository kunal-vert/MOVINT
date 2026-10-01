import React from "react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";

export interface TravelerCardProps {
  passportId: string;
  fullName: string;
  nationality: string;
  journeyStatus?: string;
  riskScore?: number;
  watchFlag?: boolean;
}

export const TravelerCard: React.FC<TravelerCardProps> = ({
  passportId,
  fullName,
  nationality,
  journeyStatus,
  riskScore,
  watchFlag,
}) => {
  return (
    <Card className="traveler-card p-4 border rounded-md">
      <div className="traveler-header flex justify-between items-center mb-2">
        <h4 className="font-bold">{fullName}</h4>
        {watchFlag && <Badge variant="danger">FLAGGED</Badge>}
      </div>
      <p className="text-sm">Passport: {passportId}</p>
      <p className="text-sm">Nationality: {nationality}</p>
      {journeyStatus && <p className="text-sm">Status: {journeyStatus}</p>}
      {riskScore !== undefined && <p className="text-sm">Risk Score: {riskScore}</p>}
    </Card>
  );
};

export default TravelerCard;
