from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.model import (
    Traveler,
    Journey,
    Permit,
    Checkpoint,
)
from app.schemas.p import (
    RegisterTravelerRequest,
    TravelerListResponse,
)
from app.utils.EnumUtili import JourneyStatus


router = APIRouter(
    prefix="/Immigration",
    tags=["Registration"],
)


# ──────────────────────────────────────────────
#  POST  /Immigration/reg
#  Register a traveler at an entry checkpoint
# ──────────────────────────────────────────────

@router.post("/reg")
def Immigration_reg(
    data: RegisterTravelerRequest,
    db: Session = Depends(get_db),
):
    """
    Register a traveler at an entry checkpoint.

    Flow
    ----
    1. Validate the entry checkpoint  (must exist, active, entry-point).
    2. Look up traveler by passport_id.
       • EXISTS  + has ACTIVE journey  → 409 Conflict
       • EXISTS  + no active journey   → returning traveler — new journey + permit
       • NOT EXISTS                    → new traveler + journey + permit
    3. Return registration summary.
    """

    # ── Step 1 : Validate the entry checkpoint ─────────────────────────
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

    # ── Step 2 : Look up traveler by passport_id ───────────────────────
    traveler = (
        db.query(Traveler)
        .filter(Traveler.passport_id == data.passport_id)
        .first()
    )

    is_returning_traveler = False
    past_journey_count = 0

    try:
        # ─────────────────────────────────────────
        #  CASE A — Traveler already in the system
        # ─────────────────────────────────────────
        if traveler:

            # Block registration if an ACTIVE journey already exists
            active_journey = (
                db.query(Journey)
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
                        "Cannot register again until the current journey is completed."
                    ),
                )

            # Count all past journeys for the returning-traveler flag
            past_journey_count = (
                db.query(Journey)
                .filter(Journey.traveler_id == traveler.id)
                .count()
            )
            is_returning_traveler = True

        # ─────────────────────────────────────────
        #  CASE B — Brand-new traveler
        # ─────────────────────────────────────────
        else:
            traveler = Traveler(
                passport_id=data.passport_id,
                nationality=data.nationality,
                full_name=data.full_name,
                date_of_birth=datetime(
                    data.date_of_birth.year,
                    data.date_of_birth.month,
                    data.date_of_birth.day,
                ),
                gender=data.gender,
                occupation=data.occupation,
                visa_type=data.visa_type,
                visa_number=data.visa_number,
                photo_url=data.photo_url,
                criminal_record=data.criminal_record,
            )
            db.add(traveler)
            db.flush()  # materialise traveler.id without committing

        # ── Step 3 : Create a new Journey (ACTIVE) ────────────────────
        now = datetime.now(timezone.utc)

        new_journey = Journey(
            traveler_id=traveler.id,
            entry_checkpoint_id=checkpoint.id,
            visa_type=data.visa_type,
            status=JourneyStatus.ACTIVE,
            current_risk_score=0,        # risk_service will recalculate later
            entered_at=now,
            expected_exit_at=data.expected_exit_at,
            declared_states=data.declared_states,
        )
        db.add(new_journey)
        db.flush()  # materialise new_journey.id

        # ── Step 4 : Create a new Permit ──────────────────────────────
        new_permit = Permit(
            traveler_id=traveler.id,
            journey_id=new_journey.id,
            type=data.permit_type,
            Permit_Occupation=data.occupation,
            issued_by=data.permit_issued_by,
            valid_from=data.permit_valid_from,
            valid_to=data.permit_valid_to,
            permitted_states=data.permit_permitted_states,
        )
        db.add(new_permit)

        # All good — commit the full transaction
        db.commit()
        db.refresh(traveler)
        db.refresh(new_journey)
        db.refresh(new_permit)

    except HTTPException:
        # Let FastAPI HTTP errors propagate untouched
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )

    # ── Step 5 : Build & return response ──────────────────────────────
    return {
        "message": (
            "Returning traveler registered successfully"
            if is_returning_traveler
            else "New traveler registered successfully"
        ),
        "is_returning_traveler": is_returning_traveler,
        "past_journey_count": past_journey_count,
        "initial_risk_score": new_journey.current_risk_score,
        "traveler": {
            "passport_id": traveler.passport_id,
            "full_name": traveler.full_name,
            "nationality": traveler.nationality,
            "date_of_birth": str(traveler.date_of_birth),
            "gender": traveler.gender,
            "photo_url": traveler.photo_url,
            "watch_flag": traveler.watch_flag,
            "criminal_record": traveler.criminal_record,
            "created_at": str(traveler.created_at),
        },
        "journey": {
            "status": new_journey.status,
            "current_risk_score": new_journey.current_risk_score,
            "entered_at": str(new_journey.entered_at),
            "exited_at": new_journey.exited_at,
            "expected_exit_at": str(new_journey.expected_exit_at),
            "declared_states": new_journey.declared_states,
            "created_at": str(new_journey.created_at),
        },
        "permit": {
            "type": new_permit.type,
            "occupation": new_permit.Permit_Occupation,
            "issued_by": new_permit.issued_by,
            "valid_from": str(new_permit.valid_from),
            "valid_to": str(new_permit.valid_to),
            "permitted_states": new_permit.permitted_states,
        },
    }


# ──────────────────────────────────────────────
#  GET  /Immigration/view
#  List all tracked nationals — sorted by most
#  recent entry, paginated (default 10)
# ──────────────────────────────────────────────

@router.get("/view", response_model=TravelerListResponse)
def Immigration_view(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Results per page"),
    status: Optional[str] = Query(default=None, description="Filter by journey status: ACTIVE, COMPLETED, OVERDUE, FLAGGED"),
    nationality: Optional[str] = Query(default=None, description="Filter by nationality"),
    watch_flag: Optional[bool] = Query(default=None, description="Filter watch-listed travelers"),
):
    """
    List all tracked nationals.

    Sorted by **most recent journey entry** — if a traveler enters again,
    they bubble to the top of the list.
    """

    # ── Subquery: TRUE lifetime stats per traveler (unfiltered by status) ──
    journey_stats = (
        db.query(
            Journey.traveler_id,
            func.max(Journey.entered_at).label("latest_entered_at"),
            func.count(Journey.id).label("total_journeys"),
        )
        .group_by(Journey.traveler_id)
        .subquery()
    )

    # ── Main query: Traveler + lifetime journey stats ──
    query = (
        db.query(
            Traveler,
            journey_stats.c.latest_entered_at,
            journey_stats.c.total_journeys,
        )
        .outerjoin(journey_stats, Traveler.id == journey_stats.c.traveler_id)
    )

    # ── Filter by journey status (INNER JOIN on matching journeys only) ──
    if status:
        status_subquery = (
            db.query(Journey.traveler_id)
            .filter(Journey.status == status)
            .distinct()
            .subquery()
        )
        query = query.join(
            status_subquery,
            Traveler.id == status_subquery.c.traveler_id,
        )

    # ── Filter by nationality ──
    if nationality:
        query = query.filter(Traveler.nationality.ilike(f"%{nationality}%"))

    # ── Filter by watch list flag ──
    if watch_flag is not None:
        query = query.filter(Traveler.watch_flag == watch_flag)

    # ── Total count for pagination ──
    total_count = query.count()

    # ── Sort by most recent entry (DESC), NULLs last ──
    query = query.order_by(
        desc(journey_stats.c.latest_entered_at).nullslast()
    )

    # ── Paginate ──
    offset = (page - 1) * per_page
    results = query.offset(offset).limit(per_page).all()

    # ── Batch fetch latest journey for this page's travelers (avoids N+1 queries) ──
    traveler_ids = [traveler.id for traveler, _, _ in results]
    latest_journey_map = {}

    if traveler_ids:
        page_journeys = (
            db.query(Journey)
            .filter(Journey.traveler_id.in_(traveler_ids))
            .order_by(Journey.entered_at.desc())
            .all()
        )
        # Retain the most recent journey per traveler
        for j in page_journeys:
            if j.traveler_id not in latest_journey_map:
                latest_journey_map[j.traveler_id] = j

    # ── Build response rows conforming to TravelerSummary ──
    travelers_out = []

    for traveler, latest_entered_at, total_journeys in results:
        latest_journey = latest_journey_map.get(traveler.id)

        travelers_out.append({
            "passport_id": traveler.passport_id,
            "full_name": traveler.full_name,
            "nationality": traveler.nationality,
            "watch_flag": traveler.watch_flag,
            "criminal_record": traveler.criminal_record,
            "current_journey_status": latest_journey.status if latest_journey else None,
            "current_risk_score": latest_journey.current_risk_score if latest_journey else None,
            "total_journeys": total_journeys or 0,
            "entered_at": latest_entered_at,
            "expected_exit_at": latest_journey.expected_exit_at if latest_journey else None,
        })

    return {
        "total_count": total_count,
        "page": page,
        "per_page": per_page,
        "travelers": travelers_out,
    }


# ──────────────────────────────────────────────
#  GET  /Immigration/view/{passport_id}
#  View a single traveler by passport ID
# ──────────────────────────────────────────────

@router.get("/view/{passport_id}")
def Immigration_view_by_passport(passport_id: str, db: Session = Depends(get_db)):
    pass
