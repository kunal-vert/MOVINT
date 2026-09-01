from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings


# This wil be for  PostgreSQL — PostGIS ready (for future spatial queries)..... already we have written im postGIS for leaflet js



engine = create_engine(settings.POSTGRS_URL , pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

class Base (DeclarativeBase):
    pass

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 