"""
FastAPI Application Factory (India-focused Election Assistant)
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

from .config import config
from .routes.chat import router as chat_router
from .routes.timeline import router as timeline_router
from .routes.steps import router as steps_router


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title="Election Guide AI 🇮🇳",
        version="1.0.0",
        description="AI-powered assistant to understand elections, voting, and timelines in India"
    )

    # -----------------------------
    # 🌐 CORS CONFIG
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if config.DEBUG else ["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # 📡 ROUTES
    # -----------------------------
    app.include_router(chat_router)
    app.include_router(timeline_router)
    app.include_router(steps_router)

    # -----------------------------
    # 📁 STATIC FILES
    # -----------------------------
    base_dir = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, "static")
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # -----------------------------
    # 🏠 FRONTEND
    # -----------------------------
    @app.get("/", response_class=HTMLResponse)
    async def get_frontend():
        index_path = os.path.join(templates_dir, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                return f.read()

        return """
        <h1>🇮🇳 Election Guide AI</h1>
        <p>Frontend not found. Please check templates/index.html</p>
        """

    # -----------------------------
    # ❤️ HEALTH CHECK (VERY IMPORTANT)
    # -----------------------------
    @app.get("/health")
    async def health_check():
        return {
            "status": "ok",
            "app": "Election Guide AI",
            "mode": config.DEFAULT_MODE,
            "ai_enabled": config.ENABLE_AI
        }

    # -----------------------------
    # 📊 APP INFO (FOR DEBUG / DEMO)
    # -----------------------------
    @app.get("/info")
    async def app_info():
        return JSONResponse({
            "name": "Election Guide AI",
            "country": config.ELECTION_COUNTRY,
            "default_mode": config.DEFAULT_MODE,
            "supported_modes": config.SUPPORTED_MODES,
            "environment": config.ENV
        })

    return app


# Uvicorn entry point
app = create_app()