from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirmPassword: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str

class ProfileUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
