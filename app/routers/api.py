from fastapi import APIRouter, HTTPException
from app.models.scale import SubmitAnswersRequest, ScaleResultResponse, Scale
from app.services.scale_loader import load_scale
from app.services.assessment_service import save_assessment
from app.services.scoring import score_scale
import uuid

router = APIRouter(prefix="/api")

@router.get("/scales/{scale_id}", response_model=Scale)
def get_scale(scale_id: str):
    #取得指定量表
    scale = load_scale(scale_id)
    if not scale:
        raise HTTPException(404, "scale not found")
    return scale

@router.post("/scales/{scale_id}/responses", response_model=ScaleResultResponse)
def submit_scale(scale_id: str, body: SubmitAnswersRequest):
    #提交量表回應並計算分數
    scale = load_scale(scale_id)
    if not scale:
        raise HTTPException(404, "scale not found")

    total, level = score_scale(scale, body.answers)

    #save result to DB
    assessment_id = save_assessment(
        scale_id = scale_id,
        version = scale.get("version", "1.0"),
        subject_id  = body.user_id,
        answers = body.answers,
        total_score = total,
        interpretation = level
    )

    #TODO:存DB
    return ScaleResultResponse(
        scale_id=scale_id,
        score=total,
        result=level    
        assessment_id = assessment_id
    )
