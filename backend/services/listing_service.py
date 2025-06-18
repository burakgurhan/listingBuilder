from main import ListingBuilderCrew
from models.product import Product
from utils.helpers import validate_url, sanitize_url
from config.settings import get_settings
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
            crew = ListingBuilderCrew(
                url=url,
                groq_api_key=self.settings.GROQ_API_KEY,
                openai_api_key=self.settings.OPENAI_API_KEY
            )
            
            result = crew.create_crew().kickoff()
            logger.info(f"Successfully analyzed URL: {url}")
            return result
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            raise

    async def get_product(self, asin: str) -> Optional[Dict]:
        """Retrieve product data from database."""
        try:
            # Database logic here - implement when needed
            pass
        except Exception as e:
            logger.error(f"Error retrieving product {asin}: {str(e)}")
            raise