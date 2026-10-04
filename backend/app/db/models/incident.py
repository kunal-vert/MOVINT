from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.EnumUtili import IncidentSeverity, IncidentType

if TYPE_CHECKING:
    from app.db.models.checkpoint_event import CheckpointEvent
    from app.db.models.journey import Journey


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
