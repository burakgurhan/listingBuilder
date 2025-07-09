from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.database.models import User #, GenerationHistory # Assuming you have a GenerationHistory model
from app.utils.helpers import (
    validate_url, sanitize_url, get_user_by_email, create_user, verify_password
)
from app.utils.jwt_utils import create_access_token
from app.utils.email_utils import send_reset_email
from app.models.auth import (
    LoginRequest, RegisterRequest, AuthResponse, ForgotPasswordRequest,
    ForgotPasswordResponse, ProfileUpdateRequest
)
from app.models.product import GenerateTextRequest, GenerateTextResponse, HistoryItem
from fastapi.security import OAuth2PasswordBearer
from typing import List
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from config.settings import get_settings, Settings
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
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    user = get_user_by_email(db, request.email)
    if not user:
        # Note: For security, you might not want to reveal if an email exists.
        # Returning a success message regardless is a common practice.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # Generate a reset link using frontend URL from settings
    reset_link = f"{settings.FRONTEND_URL}/reset-password?email={user.email}"
    send_reset_email(user.email, reset_link)
    return ForgotPasswordResponse(message="Password reset email sent successfully!")

@router.post("/generate_text", response_model=GenerateTextResponse)
def generate_text(request: GenerateTextRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    url = sanitize_url(request.url)
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format.")
    
    try:
        result = generate_listing(url)

        if not isinstance(result, dict) or "raw_output" in result:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to get structured data from ListingCrew.")

        title = result.get("title", "No Title Generated")
        description = result.get("description", "No Description Generated")
        bullet_points = result.get("bullet_points", result.get("bulletPoints", []))
        if isinstance(bullet_points, str):
            bullet_points = [bp.strip() for bp in bullet_points.split('\n') if bp.strip()] # Handle string-formatted lists

        keywords_report = result.get("keywordsReport", "No Keywords Report Generated")

        # TODO: Save the generation result to the database, associated with the current_user
        # new_history_item = GenerationHistory(
        #     user_id=current_user.id,
        #     url=url,
        #     title=title,
        #     status="completed"
        # )
        # db.add(new_history_item)
        # db.commit()

        return GenerateTextResponse(
            titles=[title] if title else [],
            description=description,
            bulletPoints=bullet_points,
            keywordsReport=keywords_report
        )
    except Exception as e:
        # Log the full error for debugging
        print(f"Error during listing generation for URL {url}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An internal error occurred: {str(e)}")

@router.get("/history", response_model=List[HistoryItem])
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # TODO: Replace with actual database query for the GenerationHistory model
    # history = db.query(GenerationHistory).filter(GenerationHistory.user_id == current_user.id).order_by(GenerationHistory.date.desc()).all()
    # return history
    return [] # Return empty list until DB model is implemented

@router.delete("/history/{item_id}", status_code=status.HTTP_200_OK)
def delete_history_item(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # TODO: Replace with actual database query
    # item_to_delete = db.query(GenerationHistory).filter(
    #     GenerationHistory.id == item_id,
    #     GenerationHistory.user_id == current_user.id
    # ).first()
    #
    # if not item_to_delete:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found.")
    #
    # db.delete(item_to_delete)
    # db.commit()
    return {"message": "History item deleted."}

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    # TODO: Fetch real subscription data from the database based on the user
    # For now, returning basic user info.
    return {
        "email": current_user.email,
        "subscription": {
            "plan": "Pro", # Mock data
            "status": "active",
            "renewalDate": "2024-12-31"
        }
    }

@router.put("/profile")
def update_profile(
    profile_data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Note: Updating the primary email is a sensitive operation.
    # This example allows it, but you may want to add extra verification.
    if profile_data.email and profile_data.email != current_user.email:
        existing_user = get_user_by_email(db, profile_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")
        current_user.email = profile_data.email

    # Example for updating other fields
    # if profile_data.full_name:
    #     current_user.full_name = profile_data.full_name

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated successfully.", "email": current_user.email}
