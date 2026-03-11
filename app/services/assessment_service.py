import json
import uuid
from typing import Dict, Any

from app.core.db import get_conn


def save_assessment(
    scale_id: str,
    version: str,
    subject_id: str | None,
    answers: Dict[str, Any],
    total_score: float,
    interpretation: str,
) -> str:
    assessment_id = str(uuid.uuid4())
    answers_json = json.dumps(answers, ensure_ascii=False)

    with get_conn() as conn:
        cur = conn.cursor()

        # Ensure scale + version exist (minimal)
        cur.execute(
            "IF NOT EXISTS (SELECT 1 FROM dbo.scales WHERE scale_id = ?) "
            "INSERT INTO dbo.scales (scale_id, name) VALUES (?, ?);",
            (scale_id, scale_id, scale_id),
        )

        cur.execute(
            "IF NOT EXISTS (SELECT 1 FROM dbo.scale_versions WHERE scale_id = ? AND version = ?) "
            "INSERT INTO dbo.scale_versions (scale_id, version, definition_json) VALUES (?, ?, ?);",
            (scale_id, version, scale_id, version, "{}"),
        )

        cur.execute(
            "INSERT INTO dbo.assessments "
            "(assessment_id, scale_id, version, subject_id, total_score, interpretation, answers_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);",
            (assessment_id, scale_id, version, subject_id, total_score, interpretation, answers_json),
        )

        for item_id, score in answers.items():
            cur.execute(
                "INSERT INTO dbo.assessment_answers "
                "(assessment_id, item_id, answer_value, score) VALUES (?, ?, ?, ?);",
                (assessment_id, item_id, str(score), float(score) if score is not None else 0.0),
            )

        conn.commit()

    return assessment_id