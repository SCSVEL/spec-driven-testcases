import sqlite3
import pytest
from starlette.testclient import TestClient


@pytest.fixture
def client():
    """TestClient backed by an in-memory SQLite database for test isolation."""
    # Import here so the fixture works once main.py exists
    from main import app, get_db

    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Initialise schema on the in-memory connection
    from database import init_db
    init_db(conn)

    # Override the dependency that provides a DB connection
    app.dependency_overrides[get_db] = lambda: conn

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    conn.close()
