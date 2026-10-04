from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.utils.EnumUtili import OfficerRole

if TYPE_CHECKING:
    from app.db.models.checkpoint import Checkpoint
    from app.db.models.checkpoint_event import CheckpointEvent


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
