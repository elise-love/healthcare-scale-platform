import os
from pathlib import Path
import pyodbc

BASE_DIR = Path(__file__).resolve().parent.parent
MSSQL_SCHEMA_PATH = Path(__file__).resolve().parent / "schema_mssql.sql"


def get_conn() -> pyodbc.Connection:
    conn_str = os.getenv("MSSQL_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError("MSSQL_CONNECTION_STRING is not set")
    # autocommit False so we can commit explicitly
    return pyodbc.connect(conn_str, autocommit=False)


def _run_schema(conn: pyodbc.Connection) -> None:
    # Split on GO batches (basic splitter)
    sql = MSSQL_SCHEMA_PATH.read_text(encoding="utf-8")
    batches = []
    current = []
    for line in sql.splitlines():
        if line.strip().upper() == "GO":
            if current:
                batches.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        batches.append("\n".join(current))

    cur = conn.cursor()
    for batch in batches:
        if batch.strip():
            cur.execute(batch)
    conn.commit()


def init_db() -> None:
    db_init = os.getenv("DB_INIT", "false").lower() == "true"
    if not db_init:
        return
    with get_conn() as conn:
        _run_schema(conn)