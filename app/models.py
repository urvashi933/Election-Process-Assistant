"""
Pydantic models for request/response validation (India-focused)
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# -----------------------------
# 🧠 INTENT TYPES (UPDATED)
# -----------------------------
class IntentType(str, Enum):
    REGISTRATION = "registration"
    TIMELINE = "timeline"
    VOTING = "voting"
    DOCUMENTS = "documents"
    POLLING = "polling"
    RESULTS = "results"
    GENERAL = "general"


# -----------------------------
# 💬 CHAT MODELS
# -----------------------------
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=500)
    session_id: Optional[str] = None
    mode: Optional[str] = "guide"   # guide | timeline | quiz


class ChatResponse(BaseModel):
    response: str
    intent: IntentType
    confidence: Optional[float] = None
    mode: Optional[str] = None

    # structured data support (important for UI)
    data: Optional[Any] = None

    follow_up_suggestions: List[str]
    sources: List[str]


# -----------------------------
# 🗓️ TIMELINE MODELS
# -----------------------------
class TimelineEvent(BaseModel):
    event: str
    description: str

    # Optional for dynamic timelines
    date: Optional[str] = None
    phase: Optional[int] = None
    days_remaining: Optional[int] = None


# -----------------------------
# 🪜 STEP-BY-STEP MODELS
# -----------------------------
class ElectionStep(BaseModel):
    step_id: str
    title: str
    description: str

    actions: List[str]
    estimated_time: str
    resources: List[str]

    # 🔥 optional UX enhancement
    next_step: Optional[str] = None


# -----------------------------
# 📊 GENERIC API RESPONSE (OPTIONAL)
# -----------------------------
class APIResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None