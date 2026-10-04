from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.EnumUtili import JourneyStatus

if TYPE_CHECKING:
    from app.db.models.alert import Alert
    from app.db.models.checkpoint import Checkpoint
    from app.db.models.checkpoint_event import CheckpointEvent
    from app.db.models.incident import Incident
    from app.db.models.permit import Permit
    from app.db.models.risk_log import RiskLog
    from app.db.models.traveler import Traveler


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
