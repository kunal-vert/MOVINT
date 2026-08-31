from fastapi import APIRouter, HTTPException,Depends,status
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.auth_model import Admin
from app.db.database import get_db
from app.schemas.auth import SignupRequest, SignInRequest
from app.utils.admin_password import password_hasher, password_verifier
from app.utils.jwt import create_access_tokens

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
        username = data.username
        email = data.email
        password = data.password

        hashed_password = password_hasher(password)

        new_admin = await Admin(
            username = username,
            email = email,
            hash_password = hashed_password,

        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return {
            "message": "Admin Successful created",
            "admin" : {
                "username": new_admin.username,
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
async def AdminSignin(data: SignInRequest,db: Session = Depends(get_db)):
    identifier = data.identifier


    admin = (
        db.query(Admin)
        .filter(
            or_(
                Admin.username == identifier,
                Admin.email == identifier
            )
        )
        .first()
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid username/email or password"

        )

    passwordverification = password_verifier(data.password == admin.hash_password)

    if not passwordverification:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    access_token  = create_access_tokens(str(admin.id))


    return {
         "message": "Admin Signin ho gaya bhaiwa :)",
        "token": access_token,
        "token_type": "bearer"

    }

             

    

        
   

        


        
        

    

    
