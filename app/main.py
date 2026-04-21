from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat_router, steps_router, timeline_router

# 1. Initialize the FastAPI application
app = FastAPI(
    title="Indian Election Guide AI",
    description="Interactive AI Assistant for Election Commission of India processes. Built for PromptWars Challenge.",
    version="1.0.0"
)

# 2. Configure CORS (Cross-Origin Resource Sharing)
# This allows your frontend (UI) to make requests to this backend API safely.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your actual frontend URL (e.g., "https://my-vercel-app.com")
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 3. Include API Routers
# This connects the endpoints defined in your app/routes/ folder to the main app.
app.include_router(chat_router)
app.include_router(steps_router)
app.include_router(timeline_router)

# 4. Health Check / Root Endpoint
# Vercel and Docker use this to check if your server is running successfully.
@app.get("/")
async def root():
    return {
        "status": "Online",
        "service": "Indian Election Assistant API",
        "fallback_system": "Active",
        "message": "Welcome to the Chunav Guide API!"
    }