from fastapi import FastAPI
from backend.app.db import model 
import backend.app.db.database as database


app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/MOVINT/V2/singup")
async def SignUp():
    return {"message": "u r singed in bruhh"}


@app.post("/MOVINT/V2/singin")
async def SignUp():
    return {"message": "u r singed in bruhh"}


@app.post("/MOVINT/V2/Traveller")
async def SignUp():
    return {"message": "u r singed in bruhh"}



@app.post("/MOVINT/V2/travellers/{passport_id}")
async def SignUp():
    return {"message": "u r singed in bruhh"}



@app.post("/MOVINT/V2/Traveller")
async def SignUp():
    return {"message": "u r singed in bruhh"}


@app.get("/MOVINT/V2/AllTracker")
async def SignUp():
    return {"message": "u r singed in bruhh"}



@app.post("MOVINT/V2/CheckPoints")
async def SignUp():
    return {"message": "u r singed in bruhh"}


@app.get("/MOVINT/V2/OnMap")
async def Onmap():
    return {"this is feature on map"}


@app.get("/MOVINT/V2/dashboard")
async def Onmap():
    return {"this is feature on map"}


@app.get("/MOVINT/V2/Alert")
async def SignUp():
    return {"message": "u r singed in bruhh"}



@app.get("/MOVINT/V2/travellers/{passport_id}/visits")
async def OneHistoryVisits():
    return {"return all the visits"}



@app.get("/MOVINT/V2/NEXUS")
async def Nexus():
    return {"this is update later while i will make the Nexus Agent "}  # this is optional yet







