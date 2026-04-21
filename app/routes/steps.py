import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.step_service import StepService

# Set up logging
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter(prefix="/api", tags=["steps"])

# Initialize the step service which contains the hardcoded ECI rules
step_service = StepService()

@router.get("/steps")
async def get_all_steps():
    """
    Retrieves all available step-by-step guides.
    Perfect for populating a grid of 'Guide Cards' on the frontend dashboard.
    """
    try:
        # Fetching all available steps and converting Pydantic models to dicts
        all_steps = [
            step_service.get_registration_steps().model_dump(),
            step_service.get_voting_steps().model_dump()
        ]
        
        return JSONResponse(content={
            "success": True, 
            "count": len(all_steps),
            "data": all_steps
        })
        
    except Exception as e:
        logger.error(f"[STEPS ERROR] Failed to fetch all steps: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch steps data.")

@router.get("/steps/{step_id}")
async def get_step(step_id: str):
    """
    Retrieves a specific step-by-step guide based on its ID.
    Valid IDs: 'register', 'voting'
    """
    try:
        # Map the incoming URL parameter to the correct service function
        steps_map = {
            "register": step_service.get_registration_steps(),
            "voting": step_service.get_voting_steps()
        }

        # If the frontend asks for a step that doesn't exist, return a clean 404 error
        if step_id not in steps_map:
            logger.warning(f"Requested unknown step ID: {step_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"Step '{step_id}' not found. Available options: {list(steps_map.keys())}"
            )

        # Return the specific step data
        return JSONResponse(content={
            "success": True, 
            "data": steps_map[step_id].model_dump()
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[STEPS ERROR] Failed to fetch step '{step_id}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching step.")