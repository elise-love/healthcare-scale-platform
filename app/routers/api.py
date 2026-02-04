from fastapi import APIRouter, HTTPException
from app.models.scale import SubmitAnswersRequest, ScaleResultResponse, Scale
from app.services.scale_loader import load_scale
from app.services.assessment_service import save_assessment
from app.services.scoring import score_scale
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

@router.get("/scales/{scale_id}", response_model=Scale)
def get_scale(scale_id: str):
    logger.info(f"GET scale Id : {scale_id}")   
    #取得指定量表
    scale = load_scale(scale_id)
    if not scale:
        logger.warning(f"Scale {scale_id} not found")
        return {"error": "scale not found"}
    return scale

@router.post("/scales/{scale_id}/responses", response_model=ScaleResultResponse)
def submit_scale(scale_id: str, body: SubmitAnswersRequest):
    logger.info(f"sumit scale {scale_id}")
    #提交量表回應並計算分數
    scale = load_scale(scale_id)
    if not scale:
        logger.warning(f"Scale {scale_id} cannot be loaded")

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
    logger.info(f"Assessment saved with ID: {assessment_id}")

    #TODO:存DB
    return ScaleResultResponse(
        scale_id=scale_id,
        score=total,
        result=level,
        assessment_id = assessment_id
    )
    logger.info(f"Scale {scale_id} result saved to DB")
