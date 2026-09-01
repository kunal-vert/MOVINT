from fastapi import FastAPI

from app.db.database import Base, engine
from app.routes.auth import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Global API prefix
app.include_router(
    admin_router,
    prefix="/MOVINT/V2"
)

app.include_router(
    
    prefix="/MOVINT/V2"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}