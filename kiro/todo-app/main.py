from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from models import TaskCreate, TaskUpdate, ReminderRequest, TaskResponse
from database import get_db, init_db, get_all_tasks, create_task, get_task, update_task, delete_task, set_reminder
from scheduler import start_scheduler, cancel_reminder, schedule_reminder

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup() -> None:
    init_db()
    start_scheduler()


@app.get("/")
def read_root() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(conn=Depends(get_db)):
    return get_all_tasks(conn)


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task_route(task: TaskCreate, conn=Depends(get_db)):
    return create_task(conn, task.title, task.description)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task: TaskUpdate, conn=Depends(get_db)):
    updated = update_task(conn, task_id, task.title, task.description)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return updated


@app.delete("/tasks/{task_id}")
def delete_task_route(task_id: int, conn=Depends(get_db)):
    deleted = delete_task(conn, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    cancel_reminder(task_id)
    return {"detail": f"Task {task_id} deleted"}


@app.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(task_id: int, conn=Depends(get_db)):
    task = get_task(conn, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    new_completed = 0 if task["completed"] else 1
    conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_completed, task_id))
    conn.commit()
    return get_task(conn, task_id)


@app.post("/tasks/{task_id}/reminder", response_model=TaskResponse)
def set_reminder_route(task_id: int, body: ReminderRequest, conn=Depends(get_db)):
    task = get_task(conn, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    remind_at_str = body.remind_at.isoformat()
    updated = set_reminder(conn, task_id, remind_at_str)

    def reminder_callback():
        import logging
        logging.getLogger(__name__).info(f"Reminder triggered for task {task_id}: {task['title']}")

    schedule_reminder(task_id, body.remind_at, reminder_callback)
    return updated
