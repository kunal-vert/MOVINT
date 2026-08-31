from fastapi import FastAPI

from app.routes.auth import router as admin_router


app = FastAPI()


# Global API prefix
app.include_router(
    admin_router,
    prefix="/MOVINT/V2"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}