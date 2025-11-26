from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.ai_controller import AIController
from models.ai_model import ToneResponse, ToneRequest

router = APIRouter(prefix="/ai_tone", tags= ["ai_tone"])

@router.post("/convert", response_model=ToneResponse)
async def tone_convert_route(request: ToneRequest):
    result = AIController.change_tone_logic(request)

    if result.tone_used == "Error":
        raise HTTPException(status_code=503, detail = "AI Service Unavailable")

    return result