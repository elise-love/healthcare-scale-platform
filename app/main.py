#app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db
from app.routers.api import router as api_router

import logging


app = FastAPI(title = "Healthcare Scale Platform")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

#CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", #vite port
        "http://localhost:3002", #CRA 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
    )

#Init DB on startup
@app.on_event("startup")
def startup():
    logger.info("Apllication starting up")
    init_db()
    logger.info("Database initialized")

#root homepage
@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"ok": True}

app.include_router(api_router)

#python -m uvicorn app.main:app --reload
#http://127.0.0.1:8000/


#Port change: main.py/ vite.config.js