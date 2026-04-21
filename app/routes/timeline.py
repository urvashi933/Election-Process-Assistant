import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.timeline_service import TimelineService

# Set up logging
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter(prefix="/api", tags=["timeline"])

# Initialize the timeline service which parses your election_knowledge.json
timeline_service = TimelineService()

@router.get("/timeline")
async def get_timeline():
    """
    Retrieves the complete election timeline and phases.
    Ideal for rendering a visual progress bar or vertical timeline on the frontend UI.
    """
    try:
        # Fetch the timeline data from the service
        timeline_data = timeline_service.get_full_timeline()
        
        # Safety check in case the JSON data is missing or corrupted
        if not timeline_data:
            logger.warning("Timeline data was requested but returned empty.")
            # We still return success: True, but with an empty list so the UI doesn't crash
            return JSONResponse(content={
                "success": True,
                "count": 0,
                "data": []
            })

        # Return the perfectly formatted list of timeline events
        return JSONResponse(content={
            "success": True,
            "count": len(timeline_data),
            "data": timeline_data
        })

    except Exception as e:
        logger.error(f"[TIMELINE ERROR] Failed to fetch timeline: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while fetching the election timeline."
        )