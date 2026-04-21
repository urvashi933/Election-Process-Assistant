from fastapi import FastAPI
from app.routes import chat_router, steps_router, timeline_router

app = FastAPI(
    title="Indian Election Guide AI",
    description="Interactive AI Assistant for the Election Commission of India processes.",
    version="1.0.0"
)

# Include Routers
app.include_router(chat_router)
app.include_router(steps_router)
app.include_router(timeline_router)

@app.get("/")
async def root():
    return {
        "status": "Online",
        "service": "Indian Election Assistant",
        "fallback_system": "Active"
    }