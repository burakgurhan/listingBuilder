import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database.models import GenerationHistory, GenerationStatus
from src.ListingCrew import main as ai_main


logger = logging.getLogger(__name__)

def process_listing_background(history_id: int, url: str):
    """
    Background worker to run CrewAI task and update DB.
    """
    db = SessionLocal()
    history_item = None  # BUG-9: Initialize to None so except block can safely reference it
    try:
        # Mark as processing
        history_item = db.query(GenerationHistory).filter(GenerationHistory.id == history_id).first()
        if not history_item:
            logger.error(f"History item {history_id} not found.")
            return

        history_item.status = GenerationStatus.processing
        db.commit()

        # Run Heavy AI Task
        result = ai_main.generate_listing(url)


        # BUG-1 FIX: Check that result is a valid dict with expected keys (inverted logic was here before)
        if not isinstance(result, dict) or "title" not in result:
            logger.error(f"Structured result failed for {url}. Got: {result}")
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
        if history_item is not None:  # BUG-9: Guard against unbound variable
            history_item.status = GenerationStatus.failed
            db.commit()
    finally:
        db.close()
