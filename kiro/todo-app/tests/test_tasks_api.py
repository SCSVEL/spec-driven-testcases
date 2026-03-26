import pytest
from datetime import datetime, timedelta, timezone


# ── helpers ──────────────────────────────────────────────────────────────────

def create(client, title="Test task", description=None):
    res = client.post("/tasks", json={"title": title, "description": description})
    assert res.status_code == 201
    return res.json()


def future_iso(seconds=120):
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


# ── create ────────────────────────────────────────────────────────────────────

def test_create_task_returns_201(client):
    res = client.post("/tasks", json={"title": "Buy milk"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert data["description"] is None
    assert data["remind_at"] is None
    assert isinstance(data["id"], int)


def test_create_task_empty_title_returns_422(client):
    res = client.post("/tasks", json={"title": ""})
    assert res.status_code == 422


def test_create_task_whitespace_title_returns_422(client):
    res = client.post("/tasks", json={"title": "   "})
    assert res.status_code == 422


def test_create_task_missing_title_returns_422(client):
    res = client.post("/tasks", json={"description": "no title"})
    assert res.status_code == 422


# ── list ──────────────────────────────────────────────────────────────────────

def test_list_tasks_empty(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.json() == []


def test_list_tasks_returns_all(client):
    create(client, "Task A")
    create(client, "Task B")
    tasks = client.get("/tasks").json()
    titles = [t["title"] for t in tasks]
    assert "Task A" in titles
    assert "Task B" in titles
    assert len(tasks) == 2


# ── update (edit/save) ────────────────────────────────────────────────────────

def test_update_task_title(client):
    task = create(client, "Original title")
    res = client.put(f"/tasks/{task['id']}", json={"title": "Updated title"})
    assert res.status_code == 200
    assert res.json()["title"] == "Updated title"


def test_update_task_description(client):
    task = create(client, "Task", description="old desc")
    res = client.put(f"/tasks/{task['id']}", json={"title": "Task", "description": "new desc"})
    assert res.status_code == 200
    assert res.json()["description"] == "new desc"


def test_update_task_clear_description(client):
    task = create(client, "Task", description="some desc")
    res = client.put(f"/tasks/{task['id']}", json={"title": "Task", "description": None})
    assert res.status_code == 200
    assert res.json()["description"] is None


def test_update_task_empty_title_returns_422(client):
    task = create(client, "Task")
    res = client.put(f"/tasks/{task['id']}", json={"title": ""})
    assert res.status_code == 422


def test_update_task_not_found_returns_404(client):
    res = client.put("/tasks/9999", json={"title": "Ghost"})
    assert res.status_code == 404


def test_update_task_persists(client):
    """Edit then re-fetch — verifies the change is actually saved."""
    task = create(client, "Before")
    client.put(f"/tasks/{task['id']}", json={"title": "After", "description": "desc"})
    tasks = client.get("/tasks").json()
    updated = next(t for t in tasks if t["id"] == task["id"])
    assert updated["title"] == "After"
    assert updated["description"] == "desc"


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_task(client):
    task = create(client, "To delete")
    res = client.delete(f"/tasks/{task['id']}")
    assert res.status_code == 200
    tasks = client.get("/tasks").json()
    assert not any(t["id"] == task["id"] for t in tasks)


def test_delete_task_not_found_returns_404(client):
    res = client.delete("/tasks/9999")
    assert res.status_code == 404


# ── complete toggle ───────────────────────────────────────────────────────────

def test_toggle_complete(client):
    task = create(client, "Toggle me")
    res = client.post(f"/tasks/{task['id']}/complete")
    assert res.status_code == 200
    assert res.json()["completed"] is True


def test_toggle_complete_twice_returns_to_original(client):
    task = create(client, "Toggle twice")
    client.post(f"/tasks/{task['id']}/complete")
    res = client.post(f"/tasks/{task['id']}/complete")
    assert res.json()["completed"] is False


def test_toggle_complete_not_found_returns_404(client):
    res = client.post("/tasks/9999/complete")
    assert res.status_code == 404


# ── reminder ──────────────────────────────────────────────────────────────────

def test_set_reminder(client):
    task = create(client, "Remind me")
    res = client.post(f"/tasks/{task['id']}/reminder", json={"remind_at": future_iso()})
    assert res.status_code == 200
    assert res.json()["remind_at"] is not None


def test_set_reminder_past_datetime_returns_422(client):
    task = create(client, "Past reminder")
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    res = client.post(f"/tasks/{task['id']}/reminder", json={"remind_at": past})
    assert res.status_code == 422


def test_set_reminder_not_found_returns_404(client):
    res = client.post("/tasks/9999/reminder", json={"remind_at": future_iso()})
    assert res.status_code == 404


# ── static serving ────────────────────────────────────────────────────────────

def test_root_serves_index_html(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]


def test_static_app_js(client):
    res = client.get("/static/app.js")
    assert res.status_code == 200
