#main.py
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db
from app.routers.api import router as api_router
from app.services.scale_loader import load_scale

app = FastAPI(title = "Healthcare Scale Platform")

@app.on_event("startup")
def startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", #vite
        "http://localhost:3000", #CRA 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def home():
    return {"ok": True}

router = APIRouter(prefix="/api")

@router.get("/scales/{scale_id}")
def get_scale(scale_id: str):
    scale = load_scale(scale_id)
    if not scale:
        raise HTTPException(404, "scale not found")
    return scale

#api
app.include_router(api_router)


#python -m uvicorn app.main:app --reload
#http://127.0.0.1:8000/
