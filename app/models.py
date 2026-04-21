from pydantic import BaseModel, Field
from typing import List, Optional

# -----------------------------
# 📥 REQUEST MODELS (Incoming Data)
# -----------------------------
class ChatRequest(BaseModel):
    """
    Schema for incoming chat messages from the frontend UI.
    """
    message: str = Field(
        ..., 
        description="The actual text message sent by the user."
    )
    session_id: Optional[str] = Field(
        default="default_session", 
        description="Used to remember conversation history (if implemented)."
    )
    country: Optional[str] = Field(
        default="India", 
        description="Ensures the context stays locked to the ECI."
    )
    mode: Optional[str] = Field(
        default="guide", 
        description="The current UI mode: 'guide', 'timeline', or 'quiz'."
    )


# -----------------------------
# 📤 RESPONSE MODELS (Outgoing Data)
# -----------------------------
class ElectionStep(BaseModel):
    """
    Schema for the structured step-by-step guidance data.
    Ensures the frontend always receives the exact same keys.
    """
    step_id: str = Field(
        ..., 
        description="Unique identifier (e.g., 'register', 'voting')."
    )
    title: str = Field(
        ..., 
        description="The main heading for the UI card."
    )
    description: str = Field(
        ..., 
        description="A short summary of what this phase entails."
    )
    actions: List[str] = Field(
        ..., 
        description="A list of bullet points for the user to follow."
    )
    estimated_time: str = Field(
        ..., 
        description="How long the process typically takes."
    )
    resources: List[str] = Field(
        ..., 
        description="Important links or apps (e.g., 'Voter Helpline App')."
    )