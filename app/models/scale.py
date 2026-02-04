from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)
    
class Interpretation(BaseModel):
    min: int
    max: int
    label: str

class Scoring(BaseModel):
    method: str
    min: int
    max: int
    interpretation: List[Interpretation]

class Option(BaseModel):
    key: str
    label: str

class Item(BaseModel):
    item_id: str
    order: int
    text: str
    reverse: bool
    weight: float

class Scale(BaseModel):
    scale_id: str
    version: str
    name: str
    short_name: str
    language: str
    timeframe: str
    scoring: Scoring
    options: List[Option]
    items: List[Item]
    scoring_map: Dict[str, Dict[str, int]]

#提交答案請求模型
class SubmitAnswersRequest(BaseModel):
    answers: Dict[str, int]  #問題ID -> 分數
    user_id: Optional[str] = None

#量表結果回應模型
class ScaleResultResponse(BaseModel):
    scale_id: str
    score: int
    result: str
    assessment_id: str  #評估記錄 ID
    message: str = "評估完成"