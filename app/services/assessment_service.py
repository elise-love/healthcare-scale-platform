import json
import uuid #create unique id for each assessment
from typing import Dict, Any
from app.core.db import get_db

def _ensure_scale_and_version(conn, scale_id: str, version: str) -> None:
    #make sure scale exists
    conn.execute("""
        IF NOT EXISTS (SELECT 1 FROM dbo.scales WHERE scale_id = ?)
        BEGIN
            INSERT INTO dbo.scales (scale_id, name) VALUES (?, ?)
        END
    """, (scale_id, scale_id, scale_id))

    #make sure scale_verson exists
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
    assessment_id = str(uuid.uuid4()) #create a UUID as primary key
    answers_json = json.dumps(answers, ensure_ascii=False) #turn answers to JSON

    #connect DB
    with get_db() as conn:
        #make sure scale/ version exits
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

        #write answer's key value into answer sheet one by one
        for item_id, score in answers.items():
            conn.execute("""
                INSERT INTO dbo.assessment_answers (
                    assessment_id, item_id, answer_value, score
                ) VALUES (?, ?, ?, ?)
            """, (assessment_id, item_id, str(score), score))

        #commit to DB
        conn.commit()

    return assessment_id