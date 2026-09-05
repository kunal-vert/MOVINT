from __future__ import annotations
from datetime import datetime, UTC
from typing import List, Optional
from enum import Enum as kunalEnum
import uuid

from sqlalchemy import( String, Boolean, Float, Index , ForeignKey,Text, text, Integer, DateTime, Date, JSON, func, Enum )
from sqlalchemy.dialects.postgresql import UUID, ARRAY,JSONB

from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.app.db.database import Base

from backend.app.utils.EnumUtili import (CheckpointType, OfficerRole, JourneyStatus, PermitType, EventStatus, IncidentType, IncidentSeverity, AlertType, AlertSeverity)


# ENUMS






class Traveler(Base):
    __tablename__ = "traveler"

    id: Mapped[uuid.UUID]          = mapped_column( UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    passport_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    nationality: Mapped[str]  = mapped_column(String(30), nullable=False)

    full_name: Mapped[str]  = mapped_column(String(50), nullable=False)

    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    gender: Mapped[Optional[str]]  = mapped_column(String(15), nullable= True, default="unknown")

    occupation: Mapped[str] = mapped_column (String(50), nullable=False) 
    # we need to be craefull => here we will update the existing occuption as traveler could be come as with different occuption for etc reason


    visa_type: Mapped[str]  = mapped_column(String(100), nullable=False)

    visa_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True, default="xxxxx")

    photo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="photo directery file")

    watch_flag: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))

    criminal_record: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())



    #relationship
    journeys: Mapped[List["Journey"]]  = relationship(
        "Journey", back_populates="traveler", foreign_keys="Journey.traveler_id"
    )


    permits: Mapped[List["Permit"]] = relationship(
        "Permit", back_populates="traveler"
    )

    alerts: Mapped[List["Alert"]] = mapped_column(
        "Alert", back_populates="traveler"
    )









#Highly crucial table dawg!
class Journey(Base):
    __tablename__ = "journey"


    id: Mapped[uuid.UUID]  = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    traveler_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("traveler.id"), nullable=False
    )


    entry_checkpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=False
    )


    exit_checkpoint_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=True
        # NULL until traveler registers at exit airport
    )



    visa_type: Mapped[str] = mapped_column( String(100), nullable=False, )



    occupation: Mapped[str]  = mapped_column(
        String(100), nullable=False
    )


    status: Mapped[str] = mapped_column(
        kunalEnum(JourneyStatus), nullable=False, default=JourneyStatus.ACTIVE
    )


    current_risk_score: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0")
    )


    entered_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )



    exited_at: Mapped[Optional[datetime]] = mapped_column(
       DateTime(timezone=True), nullable=True,
    )


    expected_exit_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        # Visa expiry or declared departure — overdue detection key
    )


    declared_states: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String), nullable=True
        # e.g. ["Manipur", "Nagaland"] — what they said they'd visit
    )

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=func.now()
    ) 

    #relationship 

    # Journey → Traveler 
    traveler:Mapped["Traveler"] = relationship( "Traveler", back_populates="journeys", foreign_keys=[traveler_id], )

     
    # Journey → Entry Checkpoint 
    entry_checkpoint: Mapped["Checkpoint"] = relationship( "Checkpoint", back_populates="entry_journeys", foreign_keys=[entry_checkpoint_id], ) 



    # Journey → Exit Checkpoint 
    exit_checkpoint: Mapped[Optional["Checkpoint"]] = relationship( "Checkpoint", back_populates="exit_journeys", foreign_keys=[exit_checkpoint_id], )




    # Journey → CheckpointEvents
    events: Mapped[list["CheckpointEvent"]] = relationship( "CheckpointEvent", back_populates="journey", )




    # Journey → Permits
    permits: Mapped[list["Permit"]] = relationship( "Permit", back_populates="journey", ) 




    # Journey → Alerts
    alerts: Mapped[list["Alert"]] = relationship( "Alert", back_populates="journey", )




    # Journey → RiskLogs 
    risk_logs: Mapped[list["RiskLog"]] = relationship( "RiskLog", back_populates="journey", )



    # Journey → Incidents
    incidents: Mapped[list["Incident"]] = relationship( "Incident", back_populates="journey", )












class Checkpoint(Base):
    __tablename__ = "checkpoint"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 
    )  

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  

    checkpoint_type: Mapped[str] = mapped_column(
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

    officers: Mapped[List["Officer"]] = relationship(
        "Officer",
        back_populates="checkpoint",
    )

    entry_journeys: Mapped[List["Journey"]] = relationship(
        "Journey",
        back_populates="entry_checkpoint",
        foreign_keys="Journey.entry_checkpoint_id",
    )

    exit_journeys: Mapped[List["Journey"]] = relationship(
        "Journey",
        back_populates="exit_checkpoint",
        foreign_keys="Journey.exit_checkpoint_id",
    )

    events: Mapped[List["CheckpointEvent"]] = relationship(
        "CheckpointEvent",
        back_populates="checkpoint",
    )






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
    traveler: Mapped["Traveler"] = relationship(
        "Traveler",
        back_populates="permits",
    )

    journey: Mapped["Journey"] = relationship(
        "Journey",
        back_populates="permits",
    )






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
    


    #We won't gonna use yet  unitl we won't test on ground battleground
    officer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
            UUID(as_uuid=True), ForeignKey("officer.id"), nullable=False
        )
    
    
    registered_at: Mapped[datetime] = mapped_column(
            DateTime, nullable=False, default=datetime.utcnow
        )
    
    
    expected_at: Mapped[Optional[datetime]] = mapped_column(
            DateTime, nullable=True
            # Expected arrival from previous checkpoint
        )
    
    
    delay_days: Mapped[int] = mapped_column(
            Integer, default=0, server_default=text("0")
            # registered_at - expected_at in days
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
    journey: Mapped["Journey"] = relationship(
        "Journey",
        back_populates="events",
    )

    checkpoint: Mapped["Checkpoint"] = relationship(
        "Checkpoint",
        back_populates="events",
    )

    officer: Mapped[Optional["Officer"]] = relationship(
        "Officer",
        back_populates="events",
    )

    incidents: Mapped[List["Incident"]] = relationship(
        "Incident",
        back_populates="checkpoint_event",
    )

    risk_logs: Mapped[List["RiskLog"]] = relationship(
        "RiskLog",
        back_populates="checkpoint_event",
    )






class Incident(Base):
    __tablename__ = "incident"


    # this table perform things at niche although we wont' gonna write 





#System-generated. Central command reads this.
#  Backend agents write here — Overstay Watch, Movement Anomaly, etc.

class Alert(Base):
    __tablename__ = "alert"
        
    
    



    

class RiskLog(Base):
    __tablename__ = "risk_log"     

    id: Mapped[uuid.UUID]  = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ) 



    journey_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=False
    )


    checkpoint_event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint_event.id"), nullable=True
        # NULL when a scheduled agent triggers recalculation (not an event)
    )


    previous_score: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )


    risk_score: Mapped[int] = mapped_column(


        Integer, nullable=False
    )
    factors: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True
        # Full breakdown of what contributed to the score
    )


    calculated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, server_default=func.now()
    )
 
    # ── relationships ──  








   


        

 








    

