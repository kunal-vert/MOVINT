from datetime import datetime, UTC
from typing import List
from enum import Enum as kunalEnum
from sqlalchemy import( String, Boolean, Float, Index , ForeignKey, Text, Integer, DateTime, Date, JSON )

from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

from EnumUtili import (CheckpointType, OfficerRole, JourneyStatus, PermitType, EventStatus, IncidentType, IncidentSeverity, AlertType, AlertSeverity)


# ENUMS




class ForeignNational(Base):
    __tablename__ = "foreign_nationals"

    id: Mapped[int]          = mapped_column(primary_key=True)

    passport_id: Mapped[str] = mapped_column()
    

