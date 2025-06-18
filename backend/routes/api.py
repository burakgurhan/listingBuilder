from fastapi import APIRouter, HTTPException, Depends
from services.listing_service import ListingService
from models.product import Product
from typing import Dict, Optional

router = APIRouter()

@router.post("/analyze")
async def analyze_listing(url: str) -> Dict:
    """Generate SEO content for a given URL."""
    try:
        service = ListingService()
        result = await service.analyze_url(url)
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/product/{asin}")
async def get_product(asin: str) -> Optional[Dict]:
    """Retrieve product data by ASIN."""
    service = ListingService()
    product = await service.get_product(asin)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product