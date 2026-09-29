from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.EnumUtili import (
    AlertSeverity,
    AlertType,
    CheckpointType,
    EventStatus,
    IncidentSeverity,
    IncidentType,
    JourneyStatus,
    OfficerRole,
)


class Traveler(Base):
    __tablename__ = "traveler"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passport_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    nationality: Mapped[str] = mapped_column(String(30), nullable=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str | None] = mapped_column(
        String(15), nullable=True, default="unknown"
    )
    occupation: Mapped[str] = mapped_column(String(50), nullable=False)
    visa_type: Mapped[str] = mapped_column(String(100), nullable=False)
    visa_number: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True
    )
    photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    watch_flag: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    criminal_record: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    journeys: Mapped[list[Journey]] = relationship(
        back_populates="traveler", foreign_keys="Journey.traveler_id"
    )
    permits: Mapped[list[Permit]] = relationship(back_populates="traveler")
    alerts: Mapped[list[Alert]] = relationship(back_populates="traveler")


class Journey(Base):
    __tablename__ = "journey"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    traveler_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("traveler.id"), nullable=False, index=True
    )
    entry_checkpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=False
    )
    exit_checkpoint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=True
    )
    visa_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[JourneyStatus] = mapped_column(
        SQLAlchemyEnum(JourneyStatus, name="journey_status"),
        nullable=False,
        default=JourneyStatus.ACTIVE,
    )
    current_risk_score: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    entered_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    exited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    expected_exit_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    declared_states: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    traveler: Mapped[Traveler] = relationship(
        back_populates="journeys", foreign_keys=[traveler_id]
    )
    entry_checkpoint: Mapped[Checkpoint] = relationship(
        back_populates="entry_journeys", foreign_keys=[entry_checkpoint_id]
    )
    exit_checkpoint: Mapped[Checkpoint | None] = relationship(
        back_populates="exit_journeys", foreign_keys=[exit_checkpoint_id]
    )
    events: Mapped[list[CheckpointEvent]] = relationship(back_populates="journey")
    permits: Mapped[list[Permit]] = relationship(back_populates="journey")
    alerts: Mapped[list[Alert]] = relationship(back_populates="journey")
    risk_logs: Mapped[list[RiskLog]] = relationship(back_populates="journey")
    incidents: Mapped[list[Incident]] = relationship(back_populates="journey")


class Checkpoint(Base):
    __tablename__ = "checkpoint"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    checkpoint_type: Mapped[CheckpointType] = mapped_column(
        SQLAlchemyEnum(CheckpointType, name="checkpoint_type"), nullable=False
    )
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    district: Mapped[str | None] = mapped_column(String(300), nullable=True)
    is_entry_point: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    is_exit_point: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )

    officers: Mapped[list[Officer]] = relationship(back_populates="checkpoint")
    entry_journeys: Mapped[list[Journey]] = relationship(
        back_populates="entry_checkpoint", foreign_keys="Journey.entry_checkpoint_id"
    )
    exit_journeys: Mapped[list[Journey]] = relationship(
        back_populates="exit_checkpoint", foreign_keys="Journey.exit_checkpoint_id"
    )
    events: Mapped[list[CheckpointEvent]] = relationship(back_populates="checkpoint")


class Officer(Base):
    __tablename__ = "officer"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    badge_no: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    checkpoint_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=True
    )
    role: Mapped[OfficerRole] = mapped_column(
        SQLAlchemyEnum(OfficerRole, name="officer_role"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )

    checkpoint: Mapped[Checkpoint | None] = relationship(back_populates="officers")
    events: Mapped[list[CheckpointEvent]] = relationship(back_populates="officer")


class CheckpointEvent(Base):
    __tablename__ = "checkpoint_event"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    journey_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=False, index=True
    )
    checkpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint.id"), nullable=False
    )
    officer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("officer.id"), nullable=True
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    expected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delay_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    risk_score_snapshot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[EventStatus] = mapped_column(
        SQLAlchemyEnum(EventStatus, name="event_status"),
        nullable=False,
        default=EventStatus.NORMAL,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    journey: Mapped[Journey] = relationship(back_populates="events")
    checkpoint: Mapped[Checkpoint] = relationship(back_populates="events")
    officer: Mapped[Officer | None] = relationship(back_populates="events")
    incidents: Mapped[list[Incident]] = relationship(
        back_populates="checkpoint_event"
    )
    risk_logs: Mapped[list[RiskLog]] = relationship(
        back_populates="checkpoint_event"
    )


class Permit(Base):
    __tablename__ = "permit"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    traveler_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("traveler.id"), nullable=False, index=True
    )
    journey_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=True
    )
    type: Mapped[str | None] = mapped_column(String(200), nullable=True)
    Permit_Occupation: Mapped[str] = mapped_column(String(200), nullable=False)
    issued_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    valid_to: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    permitted_states: Mapped[list[str] | None] = mapped_column(
        ARRAY(String), nullable=True
    )

    traveler: Mapped[Traveler] = relationship(back_populates="permits")
    journey: Mapped[Journey | None] = relationship(back_populates="permits")


class Incident(Base):
    __tablename__ = "incident"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    journey_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=False, index=True
    )
    checkpoint_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint_event.id"), nullable=True
    )
    type: Mapped[IncidentType] = mapped_column(
        SQLAlchemyEnum(IncidentType, name="incident_type"), nullable=False
    )
    severity: Mapped[IncidentSeverity] = mapped_column(
        SQLAlchemyEnum(IncidentSeverity, name="incident_severity"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reported_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    journey: Mapped[Journey] = relationship(back_populates="incidents")
    checkpoint_event: Mapped[CheckpointEvent | None] = relationship(
        back_populates="incidents"
    )


class Alert(Base):
    __tablename__ = "alert"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    traveler_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("traveler.id"), nullable=False, index=True
    )
    journey_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=True, index=True
    )
    type: Mapped[AlertType] = mapped_column(
        SQLAlchemyEnum(AlertType, name="alert_type"), nullable=False
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        SQLAlchemyEnum(AlertSeverity, name="alert_severity"), nullable=False
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    traveler: Mapped[Traveler] = relationship(back_populates="alerts")
    journey: Mapped[Journey | None] = relationship(back_populates="alerts")


class RiskLog(Base):
    __tablename__ = "risk_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    journey_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("journey.id"), nullable=False, index=True
    )
    checkpoint_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checkpoint_event.id"), nullable=True
    )
    previous_score: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    factors: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.now()
    )

    journey: Mapped[Journey] = relationship(back_populates="risk_logs")
    checkpoint_event: Mapped[CheckpointEvent | None] = relationship(
        back_populates="risk_logs"
    )
