from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.auth_model import Admin
from app.db.database import get_db
from app.schemas.auth import SignupRequest, SignInRequest
from app.utils.admin_password import password_hasher

router = APIRouter(
    prefix= "/Admin",
    tags= ['Authentication']
)

@router.post("/signup")
async def AdminSignup(
    data: SignupRequest,
    db: Session = Depends(get_db)
    ):

    try:
        adminName = data.username
        email = data.email
        password = data.password

        hashed_password = password_hasher(password)

        new_admin = Admin(
            adminName = adminName,
            Email = email,
            password = hashed_password,

        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return {
            "message": "Admin Successful created",
            "admin" : {
                "username": new_admin.adminName,
                "email": new_admin.email,
                "password": new_admin.hash_password
            }
        }

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail= "Username or email already exists"
        )   


@router.post("/signin")
async def AdminSignin(data: SignInRequest):


    return {
        "message": "Admin Signin ho gaya bhaiwa :)"
    }
