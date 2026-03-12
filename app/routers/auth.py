import uuid
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Response, Cookie
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.db import get_db
from app.core import config

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth")

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Pydantic models ──────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class VerifyRequest(BaseModel):
    token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_jwt(user_id: str, email: str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    payload = {"sub": user_id, "email": email, "exp": expire_at}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def _decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="無效或過期的登入憑證")


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
        max_age=config.JWT_EXPIRE_MINUTES * 60,
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/register", status_code=201)
def register(body: RegisterRequest):
    """Create a new user account and return a verification token (dev-friendly)."""
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="密碼至少需要 6 個字元")

    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (body.email,)
        ).fetchone()
        if existing:
            raise HTTPException(status_code=409, detail="此電子郵件已被註冊")

        user_id = str(uuid.uuid4())
        password_hash = pwd_ctx.hash(body.password)
        conn.execute(
            "INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)",
            (user_id, body.email, password_hash),
        )

        token = str(uuid.uuid4())
        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(hours=config.VERIFICATION_TOKEN_EXPIRE_HOURS)
        ).isoformat()
        conn.execute(
            "INSERT INTO email_verification_tokens (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires_at),
        )
        conn.commit()

    logger.info(f"[AUTH] New user registered: {body.email} | verification_token={token}")

    return {
        "message": "註冊成功，請驗證電子郵件",
        "verification_token": token,
        "dev_note": "開發模式：請使用此 token 呼叫 POST /api/auth/verify",
    }


@router.post("/verify")
def verify_email(body: VerifyRequest):
    """Mark a user's email as verified using the one-time token."""
    now = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        row = conn.execute(
            "SELECT user_id, expires_at, used_at FROM email_verification_tokens WHERE token = ?",
            (body.token,),
        ).fetchone()

        if not row:
            raise HTTPException(status_code=400, detail="無效的驗證 token")
        if row["used_at"]:
            raise HTTPException(status_code=400, detail="此驗證 token 已使用")
        if row["expires_at"] < now:
            raise HTTPException(status_code=400, detail="驗證 token 已過期")

        conn.execute(
            "UPDATE users SET is_verified = 1 WHERE id = ?", (row["user_id"],)
        )
        conn.execute(
            "UPDATE email_verification_tokens SET used_at = ? WHERE token = ?",
            (now, body.token),
        )
        conn.commit()

    logger.info(f"[AUTH] Email verified for user_id={row['user_id']}")
    return {"message": "電子郵件驗證成功，請登入"}


@router.post("/login")
def login(body: LoginRequest, response: Response):
    """Verify credentials and issue JWT via HttpOnly cookie."""
    with get_db() as conn:
        user = conn.execute(
            "SELECT id, email, password_hash, is_verified FROM users WHERE email = ?",
            (body.email,),
        ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="找不到此電子郵件帳號")
    if not pwd_ctx.verify(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="密碼錯誤")
    if not user["is_verified"]:
        raise HTTPException(status_code=403, detail="請先完成電子郵件驗證再登入")

    token = _make_jwt(user["id"], user["email"])
    _set_auth_cookie(response, token)
    logger.info(f"[AUTH] User logged in: {user['email']}")
    return {"message": "登入成功", "email": user["email"]}


@router.post("/logout")
def logout(response: Response):
    """Clear the auth cookie."""
    response.delete_cookie(key="access_token", httponly=True, samesite=config.COOKIE_SAMESITE)
    return {"message": "已登出"}


@router.get("/me")
def me(access_token: str | None = Cookie(default=None)):
    """Return current user info from the JWT cookie."""
    if not access_token:
        raise HTTPException(status_code=401, detail="尚未登入")
    payload = _decode_jwt(access_token)
    return {"user_id": payload["sub"], "email": payload["email"]}
