from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.utils.EnumUtili import JourneyStatus


def _utc_comparable(value: datetime) -> datetime:
    """Normalize datetimes for comparison; timezone-naive values are treated as UTC."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RegisterTravelerRequest(BaseModel):
    passport_id: str = Field(
        min_length=7,
        max_length=50,
        description="Passport identifier, for example GBP-874221X",
    )
    nationality: str = Field(
        min_length=2,
        max_length=30,
        description="Country of citizenship",
    )
    full_name: str = Field(
        min_length=2,
        max_length=50,
        description="Full name as shown on the passport",
    )
    date_of_birth: date = Field(description="Date of birth in YYYY-MM-DD format")
    gender: str | None = Field(default="unknown", max_length=15)
    photo_url: str | None = Field(
        default=None,
        description="Path to the traveler's photo, when available",
    )
    criminal_record: bool = False
    entry_checkpoint_id: UUID
    occupation: str = Field(min_length=2, max_length=50)
    visa_type: str = Field(min_length=2, max_length=100)
    visa_number: str | None = Field(default=None, max_length=100)
    permit_type: str | None = Field(default=None, max_length=200)
    permit_issued_by: str | None = Field(default=None, max_length=255)
    permit_valid_from: datetime
    permit_valid_to: datetime
    permit_permitted_states: list[str] | None = None
    declared_states: list[str] | None = None
    expected_exit_at: datetime

    @field_validator("passport_id")
    @classmethod
    def normalize_passport_id(cls, value: str) -> str:
        value = value.strip().upper()
        if not 7 <= len(value) <= 50:
            raise ValueError("passport_id must contain between 7 and 50 characters")
        return value

    @field_validator("nationality", "full_name", "occupation", "visa_type")
    @classmethod
    def strip_and_validate_text(cls, value: str, info: Any) -> str:
        value = value.strip()
        limits = {
            "nationality": (2, 30),
            "full_name": (2, 50),
            "occupation": (2, 50),
            "visa_type": (2, 100),
        }
        minimum, maximum = limits[info.field_name]
        if not minimum <= len(value) <= maximum:
            raise ValueError(
                f"{info.field_name} must contain between {minimum} and {maximum} characters"
            )
        return value

    @field_validator("date_of_birth")
    @classmethod
    def traveler_must_be_at_least_18(cls, value: date) -> date:
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise ValueError("Traveler must be at least 18 years old")
        return value

    @field_validator("expected_exit_at")
    @classmethod
    def exit_must_be_in_future(cls, value: datetime) -> datetime:
        if _utc_comparable(value) <= datetime.now(timezone.utc):
            raise ValueError("expected_exit_at must be a future datetime")
        return value

    @field_validator("permit_valid_from", "permit_valid_to")
    @classmethod
    def permit_dates_to_naive_utc(cls, value: datetime) -> datetime:
        # The Permit model stores these fields as timezone-naive timestamps.
        return _utc_comparable(value).replace(tzinfo=None)

    @model_validator(mode="after")
    def permit_dates_must_be_ordered(self) -> RegisterTravelerRequest:
        if _utc_comparable(self.permit_valid_to) <= _utc_comparable(
            self.permit_valid_from
        ):
            raise ValueError("permit_valid_to must be after permit_valid_from")
        return self


class TravelerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    passport_id: str
    full_name: str
    nationality: str
    date_of_birth: datetime
    gender: str | None
    occupation: str
    visa_type: str
    visa_number: str | None
    photo_url: str | None
    watch_flag: bool
    criminal_record: bool
    created_at: datetime


class PermitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    journey_id: UUID | None = None
    type: str | None
    occupation: str = Field(
        validation_alias=AliasChoices("occupation", "Permit_Occupation")
    )
    issued_by: str | None
    valid_from: datetime = Field(
        validation_alias=AliasChoices("valid_from", "permit_valid_from")
    )
    valid_to: datetime = Field(
        validation_alias=AliasChoices("valid_to", "permit_valid_to")
    )
    permitted_states: list[str] | None


class JourneyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    status: JourneyStatus
    current_risk_score: int
    entry_checkpoint_id: UUID | None = None
    exit_checkpoint_id: UUID | None = None
    entered_at: datetime
    exited_at: datetime | None
    expected_exit_at: datetime
    declared_states: list[str] | None
    created_at: datetime


class TravelerDetailsResponse(BaseModel):
    traveler: TravelerOut
    journeys: list[JourneyOut]
    permits: list[PermitOut]


class RegisterTravelerResponse(TravelerDetailsResponse):
    is_returning_traveler: bool
    past_journey_count: int
    initial_risk_score: int
    message: str


class TravelerSummary(BaseModel):
    """A lightweight traveler row for the tracking view."""

    passport_id: str
    full_name: str
    nationality: str
    watch_flag: bool
    criminal_record: bool
    current_journey_status: JourneyStatus | None
    current_risk_score: int | None
    total_journeys: int
    entered_at: datetime | None
    expected_exit_at: datetime | None


class TravelerListResponse(BaseModel):
    """Paginated traveler list returned by the tracking endpoint."""

    total_count: int
    pages: int
    per_pages: int
    travelers: list[TravelerSummary]
    # people: int
