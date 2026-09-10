from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.model import (
    Traveler, 
    Journey,
    Permit,
    Checkpoint,
    CheckpointEvent
)
from app.schemas.p import RegisterTravelerRequest, RegisterTravelerResponse, TravelerOut, JourneyOut
 

router = APIRouter(
    prefix="Immigration",
    tags=["Registration"]
)


@router.post("/Immgiration/reg")
def Immgiration_reg( data: RegisterTravelerRequest,  db: Session = Depends(get_db)):

    try:

        checkpoint_check = (
            db.query(Checkpoint)
            .filter(
                Checkpoint.id == data.full_name,
                Checkpoint.is_active.is_(True),
                Checkpoint.is_entry_point == True
            )
            .first()
        )

        if Checkpoint is None:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                details = "Invalid or Inactive entry Checkpoint"
            )

    except:
        pass    


@router.get("/Immgiration/view")
def Immigration_view(db: Session = Depends(get_db)):
    pass


@router.get("/Immgiration/view/{National_id}")
def Immigration_view_National(National_id: str, db: Session = Depends(get_db)):
    pass
    





