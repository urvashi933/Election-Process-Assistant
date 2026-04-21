from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import ChatRequest
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/api", tags=["chat"])
assistant_service = AssistantService()

@router.post("/chat")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        result = await assistant_service.process_message(message=request.message.strip())
        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})