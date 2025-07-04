from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.database.models import User
from app.utils.helpers import (
    validate_url, sanitize_url, get_user_by_email, create_user, verify_password
)
from app.utils.jwt_utils import create_access_token
from app.utils.email_utils import send_reset_email
from app.models.auth import LoginRequest, RegisterRequest, AuthResponse, ForgotPasswordRequest, ForgotPasswordResponse
from app.models.product import GenerateTextRequest, GenerateTextResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List
from src.ListingCrew.main import generate_listing

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
def on_startup():
    init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.utils.jwt_utils import decode_access_token
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials.")
    user = get_user_by_email(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    token = create_access_token({"sub": user.email})
    return AuthResponse(access_token=token, token_type="bearer")

@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if request.password != request.confirmPassword:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.")
    if get_user_by_email(db, request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    user = create_user(db, request.email, request.password)
    token = create_access_token({"sub": user.email})
    return AuthResponse(access_token=token, token_type="bearer")

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    # Generate a fake reset link for demo
    reset_link = f"https://your-frontend.com/reset-password?email={user.email}"
    send_reset_email(user.email, reset_link)
    return ForgotPasswordResponse(message="Password reset email sent successfully!")

@router.post("/generate_text", response_model=GenerateTextResponse)
def generate_text(request: GenerateTextRequest):
    url = sanitize_url(request.url)
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format.")
    try:
        result = generate_listing(url)
        # Expecting result to be a dict with keys: title, description, bulletPoints, keywordsReport
        return GenerateTextResponse(
            titles=[result.get("title", "")],
            description=result.get("description", ""),
            bulletPoints=result.get("bullet_points", []),
            keywordsReport=result.get("keywordsReport", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ListingCrew error: {str(e)}")

# Mock history data for demonstration
generation_history = [
    {
        "id": 1,
        "url": "https://www.amazon.com/dp/B0BP7M5F3M",
        "date": "2024-01-15",
        "title": "Premium Wireless Bluetooth Headphones",
        "status": "completed"
    },
    {
        "id": 2,
        "url": "https://www.amazon.com/dp/B08N5WRWNW",
        "date": "2024-01-14",
        "title": "Smart Home Security Camera",
        "status": "completed"
    },
    {
        "id": 3,
        "url": "https://www.amazon.com/dp/B07XJ8C8F5",
        "date": "2024-01-13",
        "title": "Portable Phone Charger",
        "status": "completed"
    }
]

@router.get("/history")
def get_history(current_user: User = Depends(get_current_user)):
    # In production, filter by user
    return generation_history

@router.delete("/history/{item_id}")
def delete_history(item_id: int, current_user: User = Depends(get_current_user)):
    global generation_history
    generation_history = [item for item in generation_history if item["id"] != item_id]
    return {"message": "History item deleted."}

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    # Mock subscription data for demonstration
    subscription = {
        "plan": "Pro",
        "status": "active",
        "renewalDate": "2024-02-15",
        "daysLeft": 25,
        "generationsUsed": 157,
        "generationsLimit": 1000
    }
    return {
        "email": current_user.email,
        "subscription": subscription
    }

@router.put("/profile")
def update_profile(email: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Only email update for demo
    current_user.email = email
    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated.", "email": current_user.email}
