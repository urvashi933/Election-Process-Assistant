from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.routes import chat_router, steps_router, timeline_router
import logging
import time
import os
from starlette.middleware.base import BaseHTTPMiddleware

# -----------------------------
# ☁️ GOOGLE CLOUD LOGGING
# -----------------------------
# We integrate Google Cloud Logging to track app health and AI performance.
try:
    from google.cloud import logging as gcloud_logging
    client = gcloud_logging.Client()
    client.setup_logging()
    logging.info("Google Cloud Logging successfully initialized.")
except Exception as e:
    logging.warning(f"Google Cloud Logging not available locally (expected): {e}")

# 1. Initialize the FastAPI application with enhanced metadata
app = FastAPI(
    title="Indian Election Guide AI",
    description="Interactive AI Assistant for Election Commission of India (ECI) processes. Built for the PromptWars Challenge.",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 2. Performance Middleware: GZip compression
# Compresses responses to improve loading speed and efficiency.
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 3. Security Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with actual domain in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 4. Custom Middleware for Security Headers & Execution Time
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

app.add_middleware(SecurityHeadersMiddleware)

# 5. Static Files & Templates
# Mount the static directory for CSS, JS, and Images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# 6. Include API Routers
app.include_router(chat_router)
app.include_router(steps_router)
app.include_router(timeline_router)

# 7. Frontend / UI Route
@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def read_root(request: Request):
    """
    Serves the main interactive 'Chunav Guide' interface.
    """
    return templates.TemplateResponse(request, "index.html")

# 8. Health Check / Status Endpoint
@app.get("/api/health", tags=["system"])
async def health_check():
    """
    Service health check endpoint.
    """
    return {
        "status": "Healthy",
        "service": "Indian Election Assistant API",
        "version": "1.1.0",
        "timestamp": time.time(),
        "message": "Welcome to the Chunav Guide API!"
    }
