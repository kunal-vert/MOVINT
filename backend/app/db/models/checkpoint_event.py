from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Integer,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.EnumUtili import EventStatus

if TYPE_CHECKING:
    from app.db.models.checkpoint import Checkpoint
    from app.db.models.incident import Incident
    from app.db.models.journey import Journey
    from app.db.models.officer import Officer
    from app.db.models.risk_log import RiskLog


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
