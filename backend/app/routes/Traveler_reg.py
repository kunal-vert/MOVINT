from datetime import datetime, time, timezone
from math import ceil
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Checkpoint, Journey, Permit, Traveler
from app.schemas.p import (
    RegisterTravelerRequest,
    RegisterTravelerResponse,
    TravelerDetailsResponse,
    TravelerListResponse,
)
from app.utils.EnumUtili import JourneyStatus


router = APIRouter(prefix="/Immigration", tags=["Registration"])


def _enum_value(value: Any) -> Any:
    """Serialize SQLAlchemy/Python enum values consistently in API responses."""
    return value.value if hasattr(value, "value") else value


def _traveler_details(traveler: Traveler) -> dict[str, Any]:
    journeys = sorted(
        traveler.journeys,
        key=lambda journey: journey.entered_at or datetime.min,
        reverse=True,
    )
    permits = sorted(
        traveler.permits,
        key=lambda permit: permit.valid_from or datetime.min,
        reverse=True,
    )

    return {
        "traveler": {
            "passport_id": traveler.passport_id,
            "full_name": traveler.full_name,
            "nationality": traveler.nationality,
            "date_of_birth": traveler.date_of_birth,
            "gender": traveler.gender,
            "occupation": traveler.occupation,
            "visa_type": traveler.visa_type,
            "visa_number": traveler.visa_number,
            "photo_url": traveler.photo_url,
            "watch_flag": traveler.watch_flag,
            "criminal_record": traveler.criminal_record,
            "created_at": traveler.created_at,
        },
        "journeys": [
            {
                "id": journey.id,
                "status": _enum_value(journey.status),
                "current_risk_score": journey.current_risk_score,
                "entry_checkpoint_id": journey.entry_checkpoint_id,
                "exit_checkpoint_id": journey.exit_checkpoint_id,
                "entered_at": journey.entered_at,
                "exited_at": journey.exited_at,
                "expected_exit_at": journey.expected_exit_at,
                "declared_states": journey.declared_states,
                "created_at": journey.created_at,
            }
            for journey in journeys
        ],
        "permits": [
            {
                "id": permit.id,
                "journey_id": permit.journey_id,
                "type": permit.type,
                "occupation": permit.Permit_Occupation,
                "issued_by": permit.issued_by,
                "valid_from": permit.valid_from,
                "valid_to": permit.valid_to,
                "permitted_states": permit.permitted_states,
            }
            for permit in permits
        ],
    }


@router.post(
    "/reg",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterTravelerResponse,
)
def Immigration_reg(data: RegisterTravelerRequest, db: Session = Depends(get_db)):
    """Register a new or returning traveler and start an active journey."""
    checkpoint = (
        db.query(Checkpoint)
        .filter(
            Checkpoint.id == data.entry_checkpoint_id,
            Checkpoint.is_active.is_(True),
            Checkpoint.is_entry_point.is_(True),
        )
        .first()
    )
    if checkpoint is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or inactive entry checkpoint",
        )

    traveler = (
        db.query(Traveler)
        .filter(Traveler.passport_id == data.passport_id)
        .with_for_update()
        .first()
    )
    is_returning_traveler = traveler is not None
    past_journey_count = 0

    if traveler is not None:
        active_journey = (
            db.query(Journey.id)
            .filter(
                Journey.traveler_id == traveler.id,
                Journey.status == JourneyStatus.ACTIVE,
            )
            .first()
        )
        if active_journey:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Traveler already has an active journey. "
                    "Complete the current journey before registering again."
                ),
            )
        past_journey_count = (
            db.query(func.count(Journey.id))
            .filter(Journey.traveler_id == traveler.id)
            .scalar()
            or 0
        )

    try:
        if traveler is None:
            traveler = Traveler(
                passport_id=data.passport_id,
                nationality=data.nationality,
                full_name=data.full_name,
                date_of_birth=datetime.combine(data.date_of_birth, time.min),
                gender=data.gender,
                occupation=data.occupation,
                visa_type=data.visa_type,
                visa_number=data.visa_number,
                photo_url=data.photo_url,
                criminal_record=data.criminal_record,
            )
            db.add(traveler)
            db.flush()

        now = datetime.now(timezone.utc)
        journey = Journey(
            traveler_id=traveler.id,
            entry_checkpoint_id=checkpoint.id,
            visa_type=data.visa_type,
            status=JourneyStatus.ACTIVE,
            current_risk_score=0,
            entered_at=now,
            expected_exit_at=data.expected_exit_at,
            declared_states=data.declared_states,
        )
        db.add(journey)
        db.flush()

        permit = Permit(
            traveler_id=traveler.id,
            journey_id=journey.id,
            type=data.permit_type,
            Permit_Occupation=data.occupation,
            issued_by=data.permit_issued_by,
            valid_from=data.permit_valid_from,
            valid_to=data.permit_valid_to,
            permitted_states=data.permit_permitted_states,
        )
        db.add(permit)
        db.commit()
        db.refresh(traveler)
        db.refresh(journey)
        db.refresh(permit)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A traveler with this passport or visa is already registered",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        ) from exc

    return {
        "message": "Returning traveler registered successfully"
        if is_returning_traveler
        else "New traveler registered successfully",
        "is_returning_traveler": is_returning_traveler,
        "past_journey_count": past_journey_count,
        "initial_risk_score": journey.current_risk_score,
        **_traveler_details(traveler),
    }


@router.get("/view", response_model=TravelerListResponse)
def Immigration_view(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Results per page"),
    journey_status: JourneyStatus | None = Query(
        default=None,
        alias="status",
        description="Filter by journey status: ACTIVE, COMPLETED, OVERDUE, FLAGGED",
    ),
    nationality: str | None = Query(default=None, min_length=1),
    watch_flag: bool | None = Query(default=None),
):
    """Return travelers ordered by most recent journey, with optional filters."""
    latest_journey_time = (
        db.query(
            Journey.traveler_id.label("traveler_id"),
            func.max(Journey.entered_at).label("latest_entered_at"),
            func.count(Journey.id).label("total_journeys"),
        )
        .group_by(Journey.traveler_id)
        .subquery()
    )

    query = db.query(
        Traveler,
        latest_journey_time.c.latest_entered_at,
        latest_journey_time.c.total_journeys,
    ).outerjoin(
        latest_journey_time,
        Traveler.id == latest_journey_time.c.traveler_id,
    )

    if journey_status is not None:
        matching_travelers = (
            db.query(Journey.traveler_id)
            .filter(Journey.status == journey_status)
            .distinct()
            .subquery()
        )
        query = query.join(
            matching_travelers,
            Traveler.id == matching_travelers.c.traveler_id,
        )
    if nationality:
        query = query.filter(Traveler.nationality.ilike(f"%{nationality.strip()}%"))
    if watch_flag is not None:
        query = query.filter(Traveler.watch_flag.is_(watch_flag))

    total_count = query.count()
    results = (
        query.order_by(desc(latest_journey_time.c.latest_entered_at).nullslast())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    traveler_ids = [traveler.id for traveler, _, _ in results]
    latest_journeys: dict[Any, Journey] = {}
    if traveler_ids:
        journeys = (
            db.query(Journey)
            .filter(Journey.traveler_id.in_(traveler_ids))
            .order_by(desc(Journey.entered_at), desc(Journey.created_at))
            .all()
        )
        for journey in journeys:
            latest_journeys.setdefault(journey.traveler_id, journey)

    travelers = []
    for traveler, latest_entered_at, total_journeys in results:
        latest = latest_journeys.get(traveler.id)
        travelers.append(
            {
                "passport_id": traveler.passport_id,
                "full_name": traveler.full_name,
                "nationality": traveler.nationality,
                "watch_flag": traveler.watch_flag,
                "criminal_record": traveler.criminal_record,
                "current_journey_status": _enum_value(latest.status) if latest else None,
                "current_risk_score": latest.current_risk_score if latest else None,
                "total_journeys": total_journeys or 0,
                "entered_at": latest_entered_at,
                "expected_exit_at": latest.expected_exit_at if latest else None,
            }
        )

    return {
        "total_count": total_count,
        "pages": ceil(total_count / per_page) if total_count else 0,
        "per_pages": per_page,
        "travelers": travelers,
    }


@router.get("/view/{passport_id}", response_model=TravelerDetailsResponse)
def Immigration_view_by_passport(passport_id: str, db: Session = Depends(get_db)):
    """Return one traveler and their journey/permit history by passport ID."""
    normalized_passport_id = passport_id.strip().upper()
    traveler = (
        db.query(Traveler)
        .filter(Traveler.passport_id == normalized_passport_id)
        .first()
    )
    if traveler is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Traveler not found",
        )
    return _traveler_details(traveler)
