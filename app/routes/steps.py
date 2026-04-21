from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.step_service import StepService

router = APIRouter(prefix="/api", tags=["steps"])
step_service = StepService()

@router.get("/steps/{step_id}")
async def get_step(step_id: str):
    steps_map = {
        "register": step_service.get_registration_steps(),
        "voting": step_service.get_voting_steps()
    }

    if step_id not in steps_map:
        raise HTTPException(status_code=404, detail=f"Step '{step_id}' not found.")

    return JSONResponse(content={"success": True, "data": steps_map[step_id].model_dump()})