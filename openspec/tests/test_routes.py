"""
Route-level tests derived from specs/todo_mvp.md.
Each test covers one HTTP-layer scenario or edge case.
Uses a fresh TaskService per test via FastAPI dependency override.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app, get_service
from app.service import TaskService


@pytest.fixture(autouse=True)
def fresh_service():
    """Give every test its own isolated in-memory TaskService."""
    svc = TaskService()
    app.dependency_overrides[get_service] = lambda: svc
    yield svc
    app.dependency_overrides.clear()


client = TestClient(app, follow_redirects=True)


# ── Feature: List tasks ───────────────────────────────────────────────────────

def test_home_returns_200():
    """GET / always returns 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_shows_no_tasks_message():
    """GET / with empty list shows placeholder text."""
    response = client.get("/")
    assert "No tasks yet" in response.text


def test_home_shows_added_tasks(fresh_service):
    """GET / lists tasks that exist."""
    fresh_service.add_task("Buy milk")
    fresh_service.add_task("Read a book")

    response = client.get("/")
    assert "Buy milk" in response.text
    assert "Read a book" in response.text


def test_completed_task_has_done_styling(fresh_service):
    """GET / renders completed tasks with 'done' CSS class."""
    task = fresh_service.add_task("Buy milk")
    fresh_service.complete_task(task["id"])

    response = client.get("/")
    assert 'class="done"' in response.text


# ── Feature: Create task ──────────────────────────────────────────────────────

def test_post_task_valid_title_redirects_home():
    """POST /tasks with valid title redirects to / (303 → 200)."""
    response = client.post("/tasks", data={"title": "Buy milk"})
    assert response.status_code == 200
    assert "Buy milk" in response.text


def test_post_task_empty_title_shows_error():
    """POST /tasks with empty title redirects with validation error."""
    response = client.post("/tasks", data={"title": ""})
    assert response.status_code == 200
    assert "Title is required" in response.text


def test_post_task_whitespace_only_title_shows_error():
    """POST /tasks with whitespace-only title is treated as empty."""
    response = client.post("/tasks", data={"title": "   "})
    assert response.status_code == 200
    assert "Title is required" in response.text


def test_post_task_strips_whitespace_from_title():
    """POST /tasks with padded title stores only trimmed content."""
    response = client.post("/tasks", data={"title": "  Buy milk  "})
    assert "Buy milk" in response.text


# ── Feature: Complete task ────────────────────────────────────────────────────

def test_complete_task_redirects_and_shows_done(fresh_service):
    """POST /tasks/{id}/complete marks task as done and reflects in UI."""
    task = fresh_service.add_task("Buy milk")

    response = client.post(f"/tasks/{task['id']}/complete")
    assert response.status_code == 200
    assert 'class="done"' in response.text


def test_complete_missing_task_shows_error():
    """POST /tasks/99/complete for non-existent id shows error."""
    response = client.post("/tasks/99/complete")
    assert response.status_code == 200
    assert "Task not found" in response.text


def test_complete_non_integer_task_id_shows_error():
    """POST /tasks/abc/complete with non-integer id shows error, not 422."""
    response = client.post("/tasks/abc/complete")
    assert response.status_code == 200
    assert "Invalid task id" in response.text


def test_complete_already_completed_task_shows_error(fresh_service):
    """POST /tasks/{id}/complete on an already-done task shows error."""
    task = fresh_service.add_task("Buy milk")
    fresh_service.complete_task(task["id"])

    response = client.post(f"/tasks/{task['id']}/complete")
    assert response.status_code == 200
    assert "Task already completed" in response.text


def test_error_query_param_shown_on_home():
    """GET /?error=Some+message displays the error banner."""
    response = client.get("/?error=Something went wrong")
    assert "Something went wrong" in response.text


# ── Feature: Dark mode ───────────────────────────────────────────────────────

def test_dark_mode_toggle_button_present():
    """Home page renders a dark mode toggle button."""
    response = client.get("/")
    assert "Toggle Dark Mode" in response.text


def test_dark_mode_css_variables_present():
    """HTML includes CSS custom properties for dark and light themes."""
    response = client.get("/")
    assert "--bg-color" in response.text
    assert "--text-color" in response.text


def test_dark_mode_script_present():
    """Page includes JS that reads/writes localStorage for theme persistence."""
    response = client.get("/")
    assert "localStorage" in response.text
