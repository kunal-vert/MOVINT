from __future__ import __annotations__
from datetime import datetime, UTC
from typing import List, Optional
from enum import Enum as kunalEnum
import uuid

from sqlalchemy import( String, Boolean, Float, Index , ForeignKey,Text, text, Integer, DateTime, Date, JSON, func )
from sqlalchemy.dialects.postgresql import UUID, ARRAY,JSONB

from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

from EnumUtili import (CheckpointType, OfficerRole, JourneyStatus, PermitType, EventStatus, IncidentType, IncidentSeverity, AlertType, AlertSeverity)


# ENUMS




class Traveler(Base):
    __tablename__ = "traveler"

    id: Mapped[uuid.UUID]          = mapped_column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    passport_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    nationality: Mapped[str]  = mapped_column(String(30), nullable=False)

    full_name: Mapped[str]  = mapped_column(String(50), nullable=False)

    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    gender: Mapped[str]  = mapped_column(String(15), nullable= True, default="unknown")

    visa_type: Mapped[str]  = mapped_column(str(100), nullable=False)

    visa_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True, default="xxxxx")

    photo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="photo directery file")

    watch_flag: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))

    criminal_record: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False, server_default=text("false"))

    Entry_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())

    #relationship




class Checkpoint(Base):
    __tablename__ = "checkpoint"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 
    )  

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  

    post_Checking: Mapped[str] = mapped_column(
        kunalEnum(CheckpointType), nullable=False, default=kunalEnum(CheckpointType)
    )

    state: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    district: Mapped[Optional[str]] = mapped_column(
        String(300), nullable=True
    )

    is_entry_point: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    is_exit_point: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )


    #relationship






# this will be highly confidential cause it will intergrated to central command and rn we ain't use it unless we won't have the ground testing

class Officer(Base):
        
 








    

