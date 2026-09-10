from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.model import Traveler, Journey
from app.schemas.p import RegisterTravelerRequest, RegisterTravelerResponse, TravelerOut, JourneyOut


router = APIRouter(
    prefix="Immigration",
    tags=["Registration"]
)


@router.post("/Immgiration/reg")
def Immgiration_reg( data1: RegisterTravelerRequest,  db: Session = Depends(get_db)):
    check_exising = 


@router.get("/Immgiration/view")
def Immigration_view(db: Session = Depends(get_db)):
    pass


@router.get("/Immgiration/view/{National_id}")
def Immigration_view_National(National_id: str, db: Session = Depends(get_db)):
    pass
    





