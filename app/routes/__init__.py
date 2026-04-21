"""
Route handlers for Indian Election Assistant
Groups all API endpoints for clean importing in main.py
"""

from .chat import router as chat_router
from .steps import router as steps_router
from .timeline import router as timeline_router

# Export all routers so main.py can import them cleanly
__all__ = [
    "chat_router",
    "steps_router",
    "timeline_router"
]