from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.database.models import GenerationStatus

class GenerateTextRequest(BaseModel):
    url: str

class GenerateTextResponse(BaseModel):
    id: int
    url: str
    status: GenerationStatus
    message: str

class HistoryItemResponse(BaseModel):
    id: int
    url: str
    date: datetime
    title: Optional[str] = None
    description: Optional[str] = None
    bullet_points: Optional[str] = None
    keywords_report: Optional[str] = None
    status: GenerationStatus

    class Config:
        from_attributes = True
