from fastapi import APIRouter
from app.schemas.auth import SignupRequest

router = APIRouter(
    prefix= "/Admin",
    tags= ['Authentication']
)

@router.post("/signup")
async def AdminSignup(data: SignupRequest):

    return {
        "message": " Admin Signup Successfull bruhh!!!"
    }


@router.post("/signin")
async def AdminSignup(data):


    return {
        "message": "Admin Signin ho gaya bhaiwa :)"
    }
