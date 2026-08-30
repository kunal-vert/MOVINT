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
    


     
    
    __tablename__ = "officer"
 
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )


    badge_no: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )


    checkpoint_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=True
        # nullable: central command officers aren't tied to one checkpoint
    )

    role: Mapped[str] = mapped_column(
        kunalEnum(OfficerRole), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )



    # relationship





class CheckpointEvent(Base):
    __tablename__ = "checkpoint_event"
 
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


    journey_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=False
    )


    checkpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=False
    )


    officer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("officer.id"), nullable=False
    )


    registered_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )


    expected_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
        # Expected arrival from previous checkpoint
    )


    delay_minutes: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
        # registered_at - expected_at in minutes
    )


    risk_score_snapshot: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
        # Journey risk score at this exact moment
    )


    status: Mapped[str] = mapped_column(
        kunalEnum(EventStatus), nullable=False, default=EventStatus.NORMAL
    )

    
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )




    #relationship






class Permit (Base):
    __tablename__ = "permit"


    id:Mapped[uuid.UUID]  = mapped_column(
       UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  

    traveler_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey=("traveler.id"), nullable=False
    )

    journey_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=True
    )


     # consider here we can't take the enum we will take the wide ranger 
    type: Mapped[Optional[str]]  = mapped_column(
        String(200), nullable=True
    )

    Permit_Occupation: Mapped[str]  = mapped_column(
        String(200), nullable=False
    )


    issued_by: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
        # "State Govt of Manipur" / "MHA" / "Embassy"
    )


    valid_from: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )


    valid_to: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )

    permitted_states: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String), nullable=True
        # ["Manipur", "Nagaland"] — zone violation check at each event... Later when we will develop the Agent , this would be highly imperative
    )


    #relationship



    


        

 








    

