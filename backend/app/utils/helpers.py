import validators
from urllib.parse import urlparse
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user