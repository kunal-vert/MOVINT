from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routes.auth import router as admin_router
from app.routes.Traveler_reg import router as immigration_router

# Importing the immigration router registers its SQLAlchemy models on Base.metadata
# before create_all is called.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# The Bun development server runs on port 3000 while the API runs on port 8000.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global API prefix
app.include_router(admin_router, prefix="/MOVINT/V2")
app.include_router(immigration_router, prefix="/MOVINT/V2")


@app.get("/")
async def root():
    return {"message": "Hello World"}
