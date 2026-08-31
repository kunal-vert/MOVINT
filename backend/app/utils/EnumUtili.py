from enum import Enum as kunalEnum




class CheckpointType(str, kunalEnum ):
    AIRPORT         = "AIRPORT"
    BORDER_POST     = "BORDER_POST"
    POLICE_POST     = "POLICE_POST"
    IMMIGRATION     = "IMMIGRATION"

class OfficerRole(str, kunalEnum):
    CHECKPOINT_OFFICER = "CHECKPOINT_OFFICER"
    CENTRAL_COMMAND    = "CENTRAL_COMMAND"
    ADMIN              = "ADMIN"

class JourneyStatus(str, kunalEnum):
    ACTIVE    = "ACTIVE"
    COMPLETED = "COMPLETED"
    OVERDUE   = "OVERDUE"
    FLAGGED   = "FLAGGED"


class PermitType(str, kunalEnum):
    ILP             = "ILP"
    RAP             = "RAP"
    TOURIST_VISA    = "TOURIST_VISA"
    RESEARCH_PERMIT = "RESEARCH_PERMIT"


class EventStatus(str, kunalEnum):
    NORMAL   = "NORMAL"
    FLAGGED  = "FLAGGED"
    DETAINED = "DETAINED"
    CLEARED  = "CLEARED"
 
 
class IncidentType(str, kunalEnum):
    DOCUMENT_ISSUE  = "DOCUMENT_ISSUE"
    RESTRICTED_ZONE = "RESTRICTED_ZONE"
    BEHAVIOR        = "BEHAVIOR"
    CONTRABAND      = "CONTRABAND"
    OVERSTAY        = "OVERSTAY"
    PERMIT_EXPIRED  = "PERMIT_EXPIRED"
 
 
class IncidentSeverity(str, kunalEnum):
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"
 
 
class AlertType(str, kunalEnum):
    OVERDUE           = "OVERDUE"
    MISSING           = "MISSING"
    HIGH_RISK         = "HIGH_RISK"
    INCIDENT_REPORTED = "INCIDENT_REPORTED"
    PERMIT_EXPIRED    = "PERMIT_EXPIRED"
    ZONE_VIOLATION    = "ZONE_VIOLATION"
 
 
class AlertSeverity(str, kunalEnum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    CRITICAL = "CRITICAL"