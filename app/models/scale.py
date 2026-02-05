from pydantic import BaseModel
from typing import Dict, Any, List, Optional, Union, Literal
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
    key: Union[int, str]
    label: str
    value: Optional[int] = None

class Item(BaseModel):
    item_id: str
    order: int
    text: str
    item_type: Literal["single_choice", "multiple_choice", "text", "numeric"] = "single_choice"
    reverse: bool = False
    weight: float = 1.0
    options: Optional[List[Option]] = None  # Item-specific options
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    required: bool = True

class Scale(BaseModel):
    scale_id: str
    version: str
    name: str
    short_name: Optional[str] = None
    language: str = "zh-TW"
    timeframe: Optional[str] = None
    scoring: Scoring
    options: Optional[List[Option]] = None  
    items: List[Item]
    scoring_map: Optional[Dict[str, Dict[str, int]]] = None  # Optional


# === Submission Models ===

AnswerValue = Union[int, str, List[int], float, None]

class SubmitAnswersRequest(BaseModel):
    """
    Generic answer submission model.
    
    Examples:
      - Single choice: {"gds15_q01": 1}
      - Multi choice: {"phq9_q09": [1, 3, 5]}
      - Numeric: {"pain_scale": 7.5}
      - Text: {"comments": "feeling better"}
    """
    answers: Dict[str, AnswerValue]  
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ScaleResultResponse(BaseModel):
    scale_id: str
    score: float
    result: str
    assessment_id: str  
    message: str = "評估完成"
    details: Optional[Dict[str, Any]] = None