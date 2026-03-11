from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel, EmailStr

from app.core.auth import (
    AUTH_COOKIE_NAME,
    create_access_token,
    get_user_id_from_token,
    hash_password,
    verify_password,
)
from app.services.user_service import create_user, get_user_by_email, get_user_public_by_id

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(body: RegisterRequest, response: Response):
    if get_user_by_email(body.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    user = create_user(body.email, hash_password(body.password))

    # auto-login after register
    token = create_access_token(user["user_id"])
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,     # local dev HTTP
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24,
    )
    return {"user": user}


@router.post("/login")
def login(body: LoginRequest, response: Response):
    user = get_user_by_email(body.email)
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["user_id"])
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24,
    )
    return {"ok": True}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=AUTH_COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me")
def me(request: Request):
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_public_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"user": user}