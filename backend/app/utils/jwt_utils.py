import jwt
from datetime import datetime, timedelta
from typing import Optional
from config.settings import get_settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def _get_secret() -> str:
    # BUG-5 FIX: read secret from settings/environment instead of hardcoding
    return get_settings().JWT_SECRET_KEY

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _get_secret(), algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, _get_secret(), algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
