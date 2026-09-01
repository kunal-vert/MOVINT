from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.model import Traveler, Journey


router = APIRouter(
    prefix="Immigration",
    tags=["Registration"]
)


@router.post("/Immgiration/reg")
def Immgiration_reg( data1: Traveler, data2: Journey, db: Session = Depends(get_db)):
    pass


@router.get("/Immgiration/view")
def Immigration_view(db: Session = Depends(get_db)):
    pass
    





