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
    # TODO: Replace with actual AI/SEO logic
    return GenerateTextResponse(
        titles=[
            "Premium Wireless Bluetooth Headphones",
            "High-Quality Bluetooth Headphones for Music Lovers",
            "Long Battery Life Wireless Headphones"
        ],
        description="Experience superior sound quality with our premium wireless Bluetooth headphones. Perfect for music lovers and on-the-go listening.",
        bulletPoints=[
            "Crystal clear audio and deep bass",
            "Up to 30 hours battery life",
            "Comfortable over-ear design",
            "Built-in microphone for calls"
        ],
        keywordsReport="bluetooth headphones, wireless, premium sound, long battery, music, over-ear"
    )
