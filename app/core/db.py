import os
from pathlib import Path
import pyodbc
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

SCHEMA_MSSQL_PATH = Path(__file__).resolve().parent / "schema_mssql.sql"

def get_mssql_connection_string() -> str:
    cs = os.getenv("MSSQL_CONNECTION_STRING")
    if not cs:
        raise RuntimeError(
            "Missing MSSQL_CONNECTION_STRING. Example: "
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=65-0464700-01\\\\SQLEXPRESS;"
            "Database=healthcare_scale;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    return cs

def get_db():
    conn = pyodbc.connect(get_mssql_connection_string())
    conn.autocommit = False
    return conn

def init_db():
    init_flag = os.getenv("DB_INIT", "true").lower() in ("1", "true", "yes", "y", "on")
    if not init_flag:
        return

    schema = SCHEMA_MSSQL_PATH.read_text(encoding="utf-8")
    with get_db() as conn:
        cur = conn.cursor()
        #schema_mssql.sql 沒用 GO，所以可以直接 execute
        cur.execute(schema)
        conn.commit()