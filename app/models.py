from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"
    country: Optional[str] = "India"
    mode: Optional[str] = "guide"

class ElectionStep(BaseModel):
    step_id: str
    title: str
    description: str
    actions: List[str]
    estimated_time: str
    resources: List[str]