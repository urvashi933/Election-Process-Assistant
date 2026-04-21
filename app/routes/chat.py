import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import ChatRequest
from app.services.assistant_service import AssistantService

# Set up logging for this specific route
logger = logging.getLogger(__name__)

# Initialize the router with a prefix and tag for the Swagger UI documentation
router = APIRouter(prefix="/api", tags=["chat"])

# Initialize the core logic service
assistant_service = AssistantService()

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Main endpoint for interacting with the Indian Election Assistant.
    Accepts a user message and returns an AI-generated or fallback response.
    """
    try:
        # 1. Input Validation
        # Pydantic already checks data types, but we want to ensure the message isn't just blank spaces
        if not request.message or len(request.message.strip()) == 0:
            logger.warning("Received empty chat message.")
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # 2. Process the Message
        # We pass the validated message string to our AssistantService
        logger.info(f"Processing chat request for session: {request.session_id}")
        result = await assistant_service.process_message(message=request.message.strip())

        # 3. Format the Successful Response
        # We wrap the result in a standard JSON structure that the frontend expects
        response_payload = {
            "success": True,
            "data": result
        }
        
        return JSONResponse(content=response_payload)

    except HTTPException:
        # Re-raise HTTP exceptions so FastAPI handles them correctly (like the 400 bad request above)
        raise

    except Exception as e:
        # 4. Global Error Handling
        # If the LLM crashes or a database fails, catch it here so the server doesn't die
        logger.error(f"[CHAT ERROR] {str(e)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "message": "We encountered a temporary issue processing your request."
            }
        )