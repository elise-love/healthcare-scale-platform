import uuid
from typing import Optional, Dict, Any

from app.core.db import get_conn


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, email, password_hash, created_at FROM dbo.users WHERE email = ?",
            (email,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "user_id": str(row.user_id),
            "email": row.email,
            "password_hash": row.password_hash,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }


def get_user_public_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, email, created_at FROM dbo.users WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "user_id": str(row.user_id),
            "email": row.email,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }


def create_user(email: str, password_hash: str) -> Dict[str, Any]:
    user_id = str(uuid.uuid4())
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dbo.users (user_id, email, password_hash) VALUES (?, ?, ?)",
            (user_id, email, password_hash),
        )
        conn.commit()
    return {"user_id": user_id, "email": email}