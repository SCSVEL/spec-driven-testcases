import pytest

from app.service import TaskService


def test_add_task_with_valid_title():
    service = TaskService()

    task = service.add_task("Buy milk")

    assert task["id"] == 1
    assert task["title"] == "Buy milk"
    assert task["done"] is False

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0] == task


def test_reject_empty_title():
    service = TaskService()

    with pytest.raises(ValueError, match="Title is required"):
        service.add_task("")


def test_list_tasks_shows_all():
    service = TaskService()

    first = service.add_task("Buy milk")
    second = service.add_task("Read a book")
    service.complete_task(second["id"])

    tasks = service.list_tasks()

    assert len(tasks) == 2
    assert tasks[0]["id"] == first["id"]
    assert tasks[0]["title"] == "Buy milk"
    assert tasks[0]["done"] is False

    assert tasks[1]["id"] == second["id"]
    assert tasks[1]["title"] == "Read a book"
    assert tasks[1]["done"] is True


def test_mark_task_completed():
    service = TaskService()
    task = service.add_task("Buy milk")

    updated = service.complete_task(task["id"])

    assert updated["id"] == task["id"]
    assert updated["title"] == "Buy milk"
    assert updated["done"] is True

    tasks = service.list_tasks()
    assert tasks[0]["done"] is True


def test_complete_missing_task_id():
    service = TaskService()

    with pytest.raises(KeyError, match="Task not found"):
        service.complete_task(99)