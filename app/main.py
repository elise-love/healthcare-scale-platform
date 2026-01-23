#main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.db import init_db

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Healthcare Scale Platform</h1>"


#python -m uvicorn app.main:app --reload
#http://127.0.0.1:8000/
