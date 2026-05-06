<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.routes import chat_router, steps_router, timeline_router
import logging
import time
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

# 5. Include API Routers
app.include_router(chat_router)
app.include_router(steps_router)
app.include_router(timeline_router)

# 6. Health Check / Root Endpoint
@app.get("/", tags=["system"])
async def root():
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
=======
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# 1. Mount your static files (CSS/JS)
# Make sure your style.css and script.js are in a folder called 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # This reads your index.html and sends it to the browser
    with open(os.path.join("static", "index.html"), "r") as f:
        return f.read()
>>>>>>> f7f47d9e9034be66f53bdbff7db0a6c59a84345f
