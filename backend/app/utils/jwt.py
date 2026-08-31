from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings

JWT_KEY = settings.jwt_secret_key
JWT_ALGO = settings.jwt_algorithm


def create_access_tokens(admin_id: str):


    # for now we have neglected the time as we deploy we gonna set timer kinda less for visual
    # expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    playload = {
        # "expire_time": expire,
        "sub": admin_id
    }

    token = jwt.encode(
        playload,
        JWT_KEY,
        JWT_ALGO
        
    )

    return token

