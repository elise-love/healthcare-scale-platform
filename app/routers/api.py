from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scale_loader import load_scale
from services.scoring import score_scale

router = APIRouter(prefix="/api")

class SubmitBody(BaseModel):
    answers: dict 
    user_id: str | None = None #預設None

@router.get("/scales/{scale_id}")
def get_scale(scale_id: str):
    scale = load_scale(scale_id)
    if not scale:
        raise HTTPException(404, "scale not found")
    return scale

@router.post("/scales/{scale_id}/responses")
def submit_scale(scale_id: str, body:SubmitBody):
    scale = load_scale(scale_id)
    if not scale:
        raise HTTPException(404, "scale not found")

    total, level = score_scale(scale, body.answers)


    # TODO:存DB
    return{
        "scale_id": scale_id,
        "score": total,
        "result": level    
    }
