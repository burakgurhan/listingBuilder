from fastapi import APIRouter, HTTPException, Depends, status
from app.models.product import GenerateTextRequest, GenerateTextResponse
from app.utils.helpers import validate_url, sanitize_url

router = APIRouter()

@router.post("/generate_text", response_model=GenerateTextResponse)
def generate_text(request: GenerateTextRequest):
    url = sanitize_url(request.url)
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format.")

    # TODO: Replace with actual AI/SEO logic
    # For now, return mock data
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
