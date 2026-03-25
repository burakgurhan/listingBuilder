import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database.models import GenerationHistory, GenerationStatus
from src.ListingCrew.main import generate_listing

logger = logging.getLogger(__name__)

def process_listing_background(history_id: int, url: str):
    """
    Background worker to run CrewAI task and update DB.
    """
    db = SessionLocal()
    try:
        # Mark as processing
        history_item = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
        if not history_item:
            logger.error(f"History item {history_id} not found.")
            return

        history_item.status = GenerationStatus.processing
        db.commit()

        # Run Heavy AI Task
        result = generate_listing(url)

        if not isinstance(result, dict) or "raw_output" in result:
            logger.error(f"Structured result failed for {url}")
            history_item.status = GenerationStatus.failed
            db.commit()
            return
            
        title = result.get("title", "No Title Generated")
        description = result.get("description", "No Description Generated")
        
        bullet_points = result.get("bullet_points", result.get("bulletPoints", []))
        if isinstance(bullet_points, list):
            bullet_points_str = "\n".join(bullet_points)
        else:
            bullet_points_str = str(bullet_points)
            
        keywords_report = result.get("keywordsReport", "No Keywords Report Generated")
        
        history_item.title = title
        history_item.description = description
        history_item.bullet_points = bullet_points_str
        history_item.keywords_report = keywords_report
        history_item.status = GenerationStatus.completed
        db.commit()

    except Exception as e:
        logger.error(f"Error processing {url}: {e}")
        history_item.status = GenerationStatus.failed
        db.commit()
    finally:
        db.close()
