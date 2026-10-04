from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.EnumUtili import CheckpointType, EventStatus


def _to_naive_utc(value: datetime | None) -> datetime | None:
    """CheckpointEvent datetime columns are timezone-naive; store them as naive UTC."""
    if value is None:
        return None
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------
# Only `location` from the incoming payload maps to a Checkpoint column.
# Other Checkpoint columns (name, checkpoint_type, is_entry_point,
# is_exit_point, is_active) have no incoming field and are therefore NOT
# accepted on create/update until confirmed.


class CheckpointBase(BaseModel):
    # Checkpoint.location: String(50), nullable=False
    location: str = Field(max_length=50)


class CheckpointCreate(CheckpointBase):
    pass


class CheckpointUpdate(BaseModel):
    location: str | None = Field(default=None, max_length=50)


class CheckpointRead(CheckpointBase):
    """Response schema mirroring the Checkpoint table (it has no timestamp columns)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    checkpoint_type: CheckpointType
    is_entry_point: bool
    is_exit_point: bool
    is_active: bool


# ---------------------------------------------------------------------------
# CheckpointEvent
# ---------------------------------------------------------------------------
# Only `expected date and time` from the incoming payload maps to a
# CheckpointEvent column (expected_at). Actual entry/exit times, passport ID
# and issues have no matching column and are intentionally omitted.


class CheckpointEventBase(BaseModel):
    # CheckpointEvent.expected_at: DateTime (naive), nullable=True
    expected_at: datetime | None = None

    @field_validator("expected_at")
    @classmethod
    def expected_at_to_naive_utc(cls, value: datetime | None) -> datetime | None:
        return _to_naive_utc(value)


class CheckpointEventCreate(CheckpointEventBase):
    pass


class CheckpointEventRead(CheckpointEventBase):
    """Response schema mirroring the checkpoint_event table."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    journey_id: UUID
    checkpoint_id: UUID
    officer_id: UUID | None
    registered_at: datetime
    delay_minutes: int
    risk_score_snapshot: int | None
    status: EventStatus
    notes: str | None
