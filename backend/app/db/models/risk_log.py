from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.checkpoint_event import CheckpointEvent
    from app.db.models.journey import Journey


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
