from src.ListingCrew.main import generate_listing
from backend.app.database.models import GenerationHistory # Updated import path
from backend.app.utils.helpers import validate_url, sanitize_url # Updated import path
from backend.config.settings import get_settings # Updated import path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ListingService:
    def __init__(self):
        self.settings = get_settings()
    
    async def analyze_url(self, url: str) -> Dict:
        """Analyze URL and generate SEO content."""
        url = sanitize_url(url)
        if not validate_url(url):
            raise ValueError("Invalid URL provided")
            
        try:
            # Using the main generate_listing function which uses ListingCrew
            result = generate_listing(url)
            logger.info(f"Successfully analyzed URL: {url}")
            return result
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            raise

    async def get_product(self, item_id: int) -> Optional[Dict]:
        """Retrieve product data from database history."""
        try:
            from backend.app.database import SessionLocal
            db = SessionLocal()
            try:
                item = db.query(GenerationHistory).filter(GenerationHistory.id == item_id).first()
                if item:
                    return {
                        "id": item.id,
                        "url": item.url,
                        "title": item.title,
                        "description": item.description,
                        "bullet_points": item.bullet_points,
                        "status": item.status
                    }
                return None
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error retrieving product {item_id}: {str(e)}")
            raise