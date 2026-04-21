"""
Step-by-step guidance endpoints (India-focused)
Aligned with Election Commission of India processes
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..services.step_service import StepService

router = APIRouter(prefix="/api", tags=["steps"])
step_service = StepService()


@router.get("/steps")
async def get_all_steps():
    """
    Get all available step-by-step guides
    """
    try:
        steps = step_service.get_all_steps()

        return JSONResponse(content={
            "success": True,
            "count": len(steps),
            "data": [step.dict() for step in steps]
        })

    except Exception as e:
        raise HTTPException(500, f"Error fetching steps: {str(e)}")


@router.get("/steps/{step_id}")
async def get_step(step_id: str):
    """
    Get specific step-by-step guide (India election flow)

    Available step_ids:
    - register → Voter registration (Electoral Roll)
    - voting → How to vote using EVM
    - documents → Required ID proofs
    - polling → Polling booth process
    - results → Counting & results
    """

    try:
        # ✅ India-specific step mapping
        steps_map = {
            "register": step_service.get_registration_steps(),
            "voting": step_service.get_voting_steps(),
            "documents": step_service.get_document_steps(),
            "polling": step_service.get_polling_steps(),
            "results": step_service.get_results_steps()
        }

        if step_id not in steps_map:
            raise HTTPException(
                status_code=404,
                detail=f"Step '{step_id}' not found. Available: {list(steps_map.keys())}"
            )

        step_data = steps_map[step_id]

        # ✅ Structured + interactive-ready response
        return JSONResponse(content={
            "success": True,
            "step_id": step_id,
            "data": step_data.dict(),
            "next_options": [
                "Explain more",
                "Show timeline",
                "Start quiz",
                "Go to next step"
            ]
        })

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(500, f"Error fetching step: {str(e)}")