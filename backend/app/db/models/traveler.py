from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.alert import Alert
    from app.db.models.journey import Journey
    from app.db.models.permit import Permit


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
