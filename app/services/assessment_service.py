import json
import uuid
from typing import Dict, Any
from app.core.db import get_db

def _ensure_scale_and_version(conn, scale_id: str, version: str) -> None:
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM dbo.scales WHERE scale_id = ?)
        BEGIN
            INSERT INTO dbo.scales (scale_id, name) VALUES (?, ?)
        END
    """, (scale_id, scale_id, scale_id))

    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM dbo.scale_versions WHERE scale_id = ? AND version = ?)
        BEGIN
            INSERT INTO dbo.scale_versions (scale_id, version, definition_json)
            VALUES (?, ?, ?)
        END
    """, (scale_id, version, scale_id, version, "{}"))

def save_assessment(
    scale_id: str,
    version: str,
    subject_id: str | None,
    answers: Dict[str, Any],
    total_score: float,
    interpretation: str
) -> str:
    assessment_id = str(uuid.uuid4())
    answers_json = json.dumps(answers, ensure_ascii=False)

    with get_db() as conn:
        _ensure_scale_and_version(conn, scale_id, version)

        conn.execute("""
            INSERT INTO dbo.assessments (
                assessment_id, scale_id, version, subject_id,
                total_score, interpretation, answers_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id, scale_id, version, subject_id,
            total_score, interpretation, answers_json
        ))

        for item_id, score in answers.items():
            conn.execute("""
                INSERT INTO dbo.assessment_answers (
                    assessment_id, item_id, answer_value, score
                ) VALUES (?, ?, ?, ?)
            """, (assessment_id, item_id, str(score), score))

        conn.commit()

    return assessment_id