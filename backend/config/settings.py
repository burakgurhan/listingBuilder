from pydantic_settings import BaseSettings
from functools import lru_cache
import os

# Compute the .env file path relative to this file's location,
# so it works regardless of the process working directory (BUG-8 FIX)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_FILE = os.path.join(_BASE_DIR, ".env")

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_JWT_SECRET: str

    # Database
    DATABASE_URL: str = "sqlite:///./listingBuilder.db"

    # JWT — BUG-5 FIX: must be set via environment variable, not hardcoded
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"

    # API Settings
    API_V1_STR: str = "/api/v1"
    FRONTEND_URL: str = "http://localhost:3000"

    # SMTP Settings for password reset emails (BUG-4 FIX moved here)
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    class Config:
        env_file = _ENV_FILE

@lru_cache()
def get_settings() -> Settings:
    return Settings()