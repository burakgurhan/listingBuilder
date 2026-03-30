import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api
from .database import init_db
from config.settings import Settings



def create_app() -> FastAPI:
    app = FastAPI(
        title="eBay SEO Agent API",
        description="API for generating SEO-optimized listings",
        version="1.0.0"
    )

    from config.settings import get_settings
    settings = get_settings()

    # BUG-6 FIX: init_db() must be called here; @router.on_event("startup")
    # on an APIRouter is silently ignored by FastAPI.
    init_db()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            settings.FRONTEND_URL
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api.router, prefix="/api/v1")

    @app.get("/")
    def read_root():
        return {"message": "Backend is running. Use /api/v1 for API endpoints."}

    return app

app = create_app()