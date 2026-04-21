"""
Service modules for Indian Election Assistant
Structured for scalability and domain-driven design
"""

# 🧠 AI / Core Intelligence Services
from .gemini_service import GeminiService
from .intent_service import IntentService
from .assistant_service import AssistantService

# 🗳️ Election Domain Services (India-focused)
from .timeline_service import TimelineService
from .step_service import StepService
from .registration_service import RegistrationService
from .voting_service import VotingService
from .document_service import DocumentService
from .polling_service import PollingService

# 🎯 Interactive / Engagement Services
from .quiz_service import QuizService
from .interactive_service import InteractiveService

# 🔄 Export all services
__all__ = [
    # Core AI
    "GeminiService",
    "IntentService",
    "AssistantService",

    # Election domain
    "TimelineService",
    "StepService",
    "RegistrationService",
    "VotingService",
    "DocumentService",
    "PollingService",

    # Interactive features
    "QuizService",
    "InteractiveService"
]