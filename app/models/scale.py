from pydantic import BaseModel
from typing import Dict, Any, List, Optional

#量表問題模型
class ScaleQuestion(BaseModel):
    id: str
    text: str
    options: List[Dict[str, Any]]

#量表等級模型
class ScaleLevel(BaseModel):
    min: int
    max: int
    label: str
    description: Optional[str] = None

#量表模型
class Scale(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    questions: List[ScaleQuestion]
    levels: List[ScaleLevel]

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