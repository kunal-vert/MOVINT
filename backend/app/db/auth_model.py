import uuid

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationships
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime
from backend.app.db.database import Base


class Admin (Base):
    __tablename__ = "admins"



    id: Mapped[uuid.UUID]  = mapped_column(
       UUID(as_uuid=True) , primary_key=True, default=uuid.uuid4
    )

    username: Mapped[str]  = mapped_column(
        String(50), unique=True, nullable=False
    )

    email: Mapped[str]   = mapped_column(
        String(50), unique=True, nullable=False
    )

    hash_password: Mapped[str]  = mapped_column(
        String(300), nullable= False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )



