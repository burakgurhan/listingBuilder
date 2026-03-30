from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from ..database import SessionLocal, init_db
from ..database.models import User, GenerationHistory, Subscription, Plan
from ..utils.helpers import (
    validate_url, sanitize_url, verify_password, get_password_hash
)
from ..utils.jwt_utils import create_access_token
from ..utils.email_utils import send_reset_email
from ..models.auth import (
    LoginRequest, RegisterRequest, AuthResponse, ForgotPasswordRequest, UpdatePasswordRequest,
    ForgotPasswordResponse, ProfileUpdateRequest, ResetPasswordRequest
)
from ..models.product import GenerateTextRequest, GenerateTextResponse, HistoryItemResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import BackgroundTasks
from ..database.models import GenerationStatus
from ..services.ai_service import process_listing_background
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

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# NOTE: init_db() is called from app/main.py create_app() — not here,
# because @router.on_event is not supported on APIRouter instances.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from ..utils.jwt_utils import decode_access_token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials.")
    
    # Supabase JWT: 'sub' is the user UUID, 'email' is the email.
    # Our DB currently links by email.
    email = payload.get("email") or payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")
        
    user = get_user_by_email(db, email)
    if not user:
        # Lazy-create user if they exist in Supabase but not in our DB yet
        user = create_user(db, email, "SUPABASE_MANAGED") # Password doesn't matter
    return user

@router.post("/login")
def login():
    raise HTTPException(status_code=status.HTTP_410_GONE, detail="Login moved to Supabase Auth on the frontend.")

@router.post("/register")
def register():
    raise HTTPException(status_code=status.HTTP_410_GONE, detail="Registration moved to Supabase Auth on the frontend.")

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    user = get_user_by_email(db, request.email)
    # BUG-3 FIX: Always return success to avoid leaking whether an email is registered
    if user:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?email={user.email}&token=demo-token"
        send_reset_email(user.email, reset_link)
    return ForgotPasswordResponse(message="Password reset email sent successfully!")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # In a real app, verify request.token here
    if request.token != "demo-token":
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token.")

    user.hashed_password = get_password_hash(request.newPassword)
    db.add(user)
    db.commit()
    return {"message": "Password reset successfully."}

@router.post("/generate", response_model=GenerateTextResponse)
def generate_text(request: GenerateTextRequest, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    url = sanitize_url(request.url)
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format.")
    
    # Save the generation result to the database as pending
    new_history_item = GenerationHistory(
        user_id=current_user.id,
        url=url,
        title=None,
        status=GenerationStatus.pending
    )
    db.add(new_history_item)
    db.commit()
    db.refresh(new_history_item)

    # Start background execution
    background_tasks.add_task(process_listing_background, new_history_item.id, url)

    return GenerateTextResponse(
        id=new_history_item.id,
        url=url,
        status=new_history_item.status,
        message="Listing generation started in the background."
    )

@router.get("/status/{item_id}", response_model=HistoryItemResponse)
def get_task_status(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(GenerationHistory).filter(GenerationHistory.id == item_id, GenerationHistory.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Task not found")
    return item

@router.get("/history", response_model=List[HistoryItemResponse])
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Query the database for generation history belonging to the current user
    history = db.query(GenerationHistory).filter(GenerationHistory.user_id == current_user.id).order_by(GenerationHistory.date.desc()).all()
    return history

@router.delete("/history/{item_id}", status_code=status.HTTP_200_OK)
def delete_history_item(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Find the history item to delete, ensuring it belongs to the current user
    item_to_delete = db.query(GenerationHistory).filter(
        GenerationHistory.id == item_id,
        GenerationHistory.user_id == current_user.id
    ).first()

    if not item_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found.")

    db.delete(item_to_delete)
    db.commit()
    return {"message": "History item deleted."}

@router.get("/profile", response_model=dict)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch user details and subscription information
    # Assuming a 'Subscription' model exists with a foreign key to User
    # and fields like plan, status, renewal_date. Adjust according to your DB schema.
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    subscription_data = {
        "plan": "Free",  # Default plan
        "status": "inactive",
        "renewalDate": None,
    }

    if user.subscription:
        subscription_data["plan"] = user.subscription.plan
        subscription_data["status"] = user.subscription.status
        subscription_data["renewalDate"] = user.subscription.renewal_date.isoformat() if user.subscription.renewal_date else None
    else:
        # Ensure a default subscription exists in the DB or just return the default data
        # For now, we return the default data but could also create a Free subscription record here.
        pass

    return {
        "id": user.id,
        "email": user.email,
        "subscription": subscription_data,
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

@router.put("/password", status_code=status.HTTP_200_OK)
def update_password(
    request: UpdatePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(request.currentPassword, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password.")

    # BUG-2 FIX: User.get_password_hash() doesn't exist; use the imported helper directly
    current_user.hashed_password = get_password_hash(request.newPassword)
    db.add(current_user)
    db.commit()

    return {"message": "Password updated successfully."}
