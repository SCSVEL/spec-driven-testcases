from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from scheduler import cancel_reminder, schedule_reminder, start_scheduler


@pytest.fixture(autouse=True)
def fresh_scheduler():
    """Start a real BackgroundScheduler for each test and shut it down after."""
    sched = start_scheduler()
    yield sched
    sched.shutdown(wait=False)


def future(seconds: int = 60) -> datetime:
    return datetime.now() + timedelta(seconds=seconds)


def test_start_scheduler_returns_running_scheduler(fresh_scheduler):
    assert fresh_scheduler.running


def test_schedule_reminder_adds_job(fresh_scheduler):
    callback = MagicMock()
    schedule_reminder(1, future(), callback)
    assert fresh_scheduler.get_job("reminder_1") is not None


def test_schedule_reminder_replaces_existing_job(fresh_scheduler):
    callback = MagicMock()
    t1 = future(120)
    t2 = future(180)
    schedule_reminder(1, t1, callback)
    schedule_reminder(1, t2, callback)
    job = fresh_scheduler.get_job("reminder_1")
    assert job is not None
    # Only one job should exist for this task_id
    all_ids = [j.id for j in fresh_scheduler.get_jobs()]
    assert all_ids.count("reminder_1") == 1


def test_cancel_reminder_removes_job(fresh_scheduler):
    callback = MagicMock()
    schedule_reminder(2, future(), callback)
    cancel_reminder(2)
    assert fresh_scheduler.get_job("reminder_2") is None


def test_cancel_reminder_noop_when_no_job(fresh_scheduler):
    # Should not raise even if no job exists
    cancel_reminder(999)


def test_job_id_format(fresh_scheduler):
    callback = MagicMock()
    schedule_reminder(42, future(), callback)
    assert fresh_scheduler.get_job("reminder_42") is not None
