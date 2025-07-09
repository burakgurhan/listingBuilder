from pydantic import BaseModel
from typing import List, Optional
import datetime

class GenerateTextRequest(BaseModel):
    url: str

class GenerateTextResponse(BaseModel):
    titles: List[str]
    description: str
    bulletPoints: List[str]
    keywordsReport: str

class HistoryItem(BaseModel):
    id: int
    url: str
    date: datetime.datetime
    title: str
    status: str

    class Config:
        orm_mode = True
