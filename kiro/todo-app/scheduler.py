from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> BackgroundScheduler:
    """Create and start the module-level BackgroundScheduler singleton."""
    global _scheduler
    _scheduler = BackgroundScheduler()
    _scheduler.start()
    return _scheduler


def schedule_reminder(task_id: int, remind_at: datetime, callback: callable) -> None:
    """Schedule a one-time reminder job for task_id at remind_at.

    Cancels any existing job for the same task_id before registering the new one.
    """
    job_id = f"reminder_{task_id}"
    cancel_reminder(task_id)
    _scheduler.add_job(callback, trigger="date", run_date=remind_at, id=job_id)


def cancel_reminder(task_id: int) -> None:
    """Remove the reminder job for task_id. No-op if no job exists."""
    job_id = f"reminder_{task_id}"
    if _scheduler is None:
        return
    try:
        _scheduler.remove_job(job_id)
    except JobLookupError:
        pass
