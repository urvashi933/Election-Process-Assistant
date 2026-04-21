from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.timeline_service import TimelineService

router = APIRouter(prefix="/api", tags=["timeline"])
timeline_service = TimelineService()

@router.get("/timeline")
async def get_timeline():
    timeline = timeline_service.get_full_timeline()
    return JSONResponse(content={"success": True, "data": timeline})