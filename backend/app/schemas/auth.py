from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    username: str =  Field(
        min_length= 10,
        examples=["StrongPassword123!"],
        description=(
            "Username must be unique"
          )),
    Email: EmailStr
    password: str = Field(
        min_length=20,
        max_length=130,
        pattern= r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).+$",
        examples=["StrongPassword123!"],
        description=(
            "Password must contain at least one lowercase letter, "
            "one uppercase letter, one number, and one special character"
    ) )


class SignInRequest(BaseModel):
    identifier: str | EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"        