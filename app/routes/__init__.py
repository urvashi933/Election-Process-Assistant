"""
Route handlers for Indian Election Assistant
Aligned with Election Commission of India workflows
"""

# Core interaction routes
from .chat import router as chat_router
from .timeline import router as timeline_router
from .steps import router as steps_router

# India-specific election routes
from .registration import router as registration_router
from .voting import router as voting_router
from .documents import router as documents_router
from .polling import router as polling_router

# Optional advanced features (for PromptWars edge)
from .quiz import router as quiz_router
from .interactive import router as interactive_router

# Export all routers
__all__ = [
    "chat_router",
    "timeline_router",
    "steps_router",
    "registration_router",
    "voting_router",
    "documents_router",
    "polling_router",
    "quiz_router",
    "interactive_router"
]