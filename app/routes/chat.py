"""
Chat endpoint for Indian Election Assistant
Aligned with Election Commission of India workflows
"""

import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..models import ChatRequest
from ..services.assistant_service import AssistantService

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)

assistant_service = AssistantService()


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Send a message to the election assistant
    Supports:
    - Step-by-step election guidance
    - Timeline queries
    - Quiz mode
    - India-specific election info
    """
    try:
        # ✅ Validate input
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # ✅ Default context (India-focused assistant)
        user_context = {
            "country": request.country if hasattr(request, "country") else "India",
            "mode": getattr(request, "mode", "guide"),  # guide | quiz | timeline
        }

        # ✅ Process message
        result = await assistant_service.process_message(
            message=request.message.strip(),
            session_id=request.session_id,
            context=user_context
        )

        # ✅ Ensure structured response (important for frontend)
        response_payload = {
            "success": True,
            "data": result,
            "context": user_context
        }

        return JSONResponse(content=response_payload)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"[CHAT ERROR] {e}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "message": str(e)
            }
        )