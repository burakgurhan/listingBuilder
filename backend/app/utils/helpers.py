import validators
from urllib.parse import urlparse
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, validators.url(url)])
    except ValueError:
        return False

def sanitize_url(url: str) -> str:
    """Clean and normalize URL."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)