from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# This wil be for  PostgreSQL — PostGIS ready (for future spatial queries)..... already we have written im postGIS for leaflet js

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost:5432/NE_MOVINT"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

class Base (DeclarativeBase):
    pass

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 