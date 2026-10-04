from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum as SQLAlchemyEnum,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.EnumUtili import CheckpointType

if TYPE_CHECKING:
    from app.db.models.checkpoint_event import CheckpointEvent
    from app.db.models.journey import Journey
    from app.db.models.officer import Officer


class Checkpoint(Base):
    __tablename__ = "checkpoint"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    checkpoint_type: Mapped[CheckpointType] = mapped_column(
        SQLAlchemyEnum(CheckpointType, name="checkpoint_type"), nullable=False
    )
    location: Mapped[str] = mapped_column(String(50), nullable=False)
   
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
