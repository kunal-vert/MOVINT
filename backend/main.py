from fastapi import FastAPI
from db import model 
import database


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

