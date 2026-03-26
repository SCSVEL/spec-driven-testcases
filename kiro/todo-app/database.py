import sqlite3
from typing import Generator

DB_PATH = "tasks.db"

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    completed   INTEGER NOT NULL DEFAULT 0,
    remind_at   TEXT
);
"""


def init_db(conn: sqlite3.Connection | None = None) -> None:
    """Create the tasks table if it doesn't exist.

    If *conn* is provided (e.g. an in-memory connection for tests), that
    connection is used directly.  Otherwise a connection to tasks.db is
    opened, used, and closed.
    """
    if conn is not None:
        conn.row_factory = sqlite3.Row
        conn.execute(CREATE_TASKS_TABLE)
        conn.commit()
    else:
        with sqlite3.connect(DB_PATH) as _conn:
            _conn.row_factory = sqlite3.Row
            _conn.execute(CREATE_TASKS_TABLE)
            _conn.commit()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency that yields a connection to tasks.db."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def _row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a dict with completed as bool."""
    d = dict(row)
    d["completed"] = bool(d["completed"])
    return d


def create_task(conn: sqlite3.Connection, title: str, description: str | None) -> dict:
    cursor = conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _row_to_dict(row)


def get_all_tasks(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    return [_row_to_dict(r) for r in rows]


def get_task(conn: sqlite3.Connection, task_id: int) -> dict | None:
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _row_to_dict(row) if row else None


def update_task(conn: sqlite3.Connection, task_id: int, title: str, description: str | None) -> dict | None:
    conn.execute(
        "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
        (title, description, task_id),
    )
    conn.commit()
    return get_task(conn, task_id)


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount > 0


def set_reminder(conn: sqlite3.Connection, task_id: int, remind_at: str) -> dict | None:
    conn.execute(
        "UPDATE tasks SET remind_at = ? WHERE id = ?",
        (remind_at, task_id),
    )
    conn.commit()
    return get_task(conn, task_id)
