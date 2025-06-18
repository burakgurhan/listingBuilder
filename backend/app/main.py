from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api
from config.settings import Settings

def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="eBay SEO Agent API",
        description="API for generating SEO-optimized listings",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api.router, prefix="/api/v1")

    return app

app = create_app()