import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from config.settings import Settings

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def create_app() -> FastAPI:
    app = FastAPI(
        title="eBay SEO Agent API",
        description="API for generating SEO-optimized listings",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api.router, prefix="/api/v1")
    return app

app = create_app()

@app.get("/")
def read_root():
    return {"message": "Backend is running. Use /api/v1 for API endpoints."}