from pydantic import BaseModel
from typing import List

class GenerateTextRequest(BaseModel):
    url: str

class GenerateTextResponse(BaseModel):
    titles: List[str]
    description: str
    bulletPoints: List[str]
    keywordsReport: str
