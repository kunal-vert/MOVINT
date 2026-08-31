
from sqlalchemy.orm import Mapped, mapped_column, relationships
from sqlalchemy import (String, int)
from database import Base


class Admin (Base):
    id: Mapped[str]  = mapped_column(
        index=True, primary_key=True, nullable=False
    )

    username: Mapped[str]  = mapped_column(
        String(50), nullable=False
    )

    email: Mapped[str]   = mapped_column(
        String(50), nullable=False
    )

    password: Mapped[str]  = mapped_column(
        String(100), nullable= False
    )



