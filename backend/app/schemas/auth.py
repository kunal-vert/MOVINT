from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    username: str 
    Email: EmailStr
    password: str


class SignInRequest(BaseModel):
    identifier: str | EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"        