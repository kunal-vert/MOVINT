from datetime import datetime, UTC
from typing import List
from sqlalchemy import( String, Boolean, Float, Index , ForeignKey, Text, Integer, DateTime, Date, JSON )
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base




class ForeignNational(Base):
    __tablename__ = "foreign_nationals"

    id: Mapped[int]          = mapped_column(primary_key=True)

    passport_id: Mapped[str] = mapped_column()
    

