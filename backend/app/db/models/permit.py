from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.journey import Journey
    from app.db.models.traveler import Traveler


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
