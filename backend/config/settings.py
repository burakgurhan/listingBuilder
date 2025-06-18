from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    
    # Database
    DATABASE_URL: str = "mysql://user:password@localhost/listingBuilder"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()