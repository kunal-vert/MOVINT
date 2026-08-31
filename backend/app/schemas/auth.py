from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupRequest(BaseModel):
    username: str =  Field(
        min_length= 10,
        
        description=(
            "Username must be unique"
          )),
    
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["StrongPassword123!"]
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:

        if not any(char.islower() for char in password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not any(char.isupper() for char in password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not any(char.isdigit() for char in password):
            raise ValueError(
                "Password must contain at least one number"
            )

        if not any(not char.isalnum() for char in password):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return password

      
    


class SignInRequest(BaseModel):
    identifier: str | EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"        