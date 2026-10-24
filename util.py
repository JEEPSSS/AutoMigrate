"""Shared helpers: connection, running .sql files, fetching results."""
import os
import pyodbc
import config


def get_connection() -> pyodbc.Connection:
    driver = getattr(config, "driver", "ODBC Driver 17 for SQL Server")
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={config.server};"
        f"DATABASE={config.database};"
        f"UID={config.username};"
        f"PWD={config.password};"
        "Encrypt=no;TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=True)


def read_sql(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def sql_files(folder: str) -> list[str]:
    return [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.endswith(".sql")]


def execute_file(path: str, label: str = "Ran") -> None:
    """Run a script that returns no rows (DDL, INSERT, UPDATE). Raises on error."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(read_sql(path))
        while cur.nextset():          # drain all statements in the batch
            pass
        cur.close()
        print(f"{label} {path} ✅")
    finally:
        conn.close()


def fetch_file(path: str):
    """Run a SELECT script; return (column_names, rows) of the last result set."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(read_sql(path))
        cols, rows = None, []
        while True:
            if cur.description:
                cols = [c[0] for c in cur.description]
                rows = [list(r) for r in cur.fetchall()]
            if not cur.nextset():
                break
        cur.close()
        return cols, rows
    finally:
        conn.close()


def try_execute_file(path: str):
    """Run a script that may be blocked by a trigger. Returns (ok, messages_or_error)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(read_sql(path))
        msgs = [m[1] for m in (cur.messages or [])]
        while cur.nextset():
            msgs += [m[1] for m in (cur.messages or [])]
        cur.close()
        return True, msgs
    except pyodbc.Error as e:
        return False, [str(e)]
    finally:
        conn.close()
