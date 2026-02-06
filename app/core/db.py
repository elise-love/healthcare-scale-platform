import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "app.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"

#create database connection
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;") #activate foreign key 
    return conn


#initialize databse with schema
def init_db():
    schema = SCHEMA_PATH.read_text(encoding="utf-8") #load schema.sql
    with get_db() as conn:
        conn.executescript(schema)
        conn.commit()
