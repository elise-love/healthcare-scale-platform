#app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db
from app.routers.api import router as api_router

app = FastAPI(title = "Healthcare Scale Platform")

#CORS 
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

#Init DB on startup
@app.on_event("startup")
def startup():
    init_db()
    init_db()

#root homepage
@app.get("/")
def home():
    return {"ok": True}

app.include_router(api_router)

#python -m uvicorn app.main:app --reload
#http://127.0.0.1:8000/