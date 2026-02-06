import json
import uuid
from datetime import datetime
from typing import Dict, Any
from app.core.db import get_db

def save_assessment(
    scale_id: str,
    version: str,
    subject_id: str | None,
    answers: Dict[str, Any],
    total_score: float,
    interpretation: str
) -> str:
    """
    儲存評估結果到資料庫
    
    Args:
        scale_id: 量表 ID
        version: 量表版本
        subject_id: 受測者 ID（可選）
        answers: 答案字典 {item_id: score}
        total_score: 總分
        interpretation: 結果解釋
    
    Returns:
        assessment_id: 評估記錄 ID
    """
    assessment_id = str(uuid.uuid4())
    answers_json = json.dumps(answers, ensure_ascii=False)
    
    with get_db() as conn:

        conn.execute("""
            INSERT OR IGNORE INTO scales (scale_id, name)
            VALUES (?, ?)
        """, (scale_id, scale_id))
        
        conn.execute("""
            INSERT OR IGNORE INTO scale_versions (scale_id, version, definition_json)
            VALUES (?, ?, ?)
        """, (scale_id, version, '{}'))
        
        conn.execute("""
            INSERT INTO assessments (
                assessment_id, scale_id, version, subject_id,
                total_score, interpretation, answers_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id, scale_id, version, subject_id,
            total_score, interpretation, answers_json
        ))
        
        # 插入個別答案記錄
        for item_id, score in answers.items():
            conn.execute("""
                INSERT INTO assessment_answers (
                    assessment_id, item_id, answer_value, score
                ) VALUES (?, ?, ?, ?)
            """, (assessment_id, item_id, str(score), score))
        
        conn.commit()
    
    return assessment_id