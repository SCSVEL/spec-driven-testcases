from __future__ import annotations

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.service import TaskService

app = FastAPI(title="ToDo OpenSpec App")
templates = Jinja2Templates(directory="templates")

_service = TaskService()


def get_service() -> TaskService:
    return _service


@app.get("/")
def home(request: Request, error: str | None = None, svc: TaskService = Depends(get_service)):
    tasks = svc.list_tasks()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "tasks": tasks, "error": error},
    )


@app.post("/tasks")
def create_task(title: str = Form(default=""), svc: TaskService = Depends(get_service)):
    try:
        svc.add_task(title)
        return RedirectResponse(url="/", status_code=303)
    except ValueError as exc:
        error = str(exc)
        return RedirectResponse(url=f"/?error={error}", status_code=303)


@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: str, svc: TaskService = Depends(get_service)):
    try:
        tid = int(task_id)
    except ValueError:
        return RedirectResponse(url="/?error=Invalid task id", status_code=303)
    try:
        svc.complete_task(tid)
        return RedirectResponse(url="/", status_code=303)
    except (KeyError, ValueError) as exc:
        error = str(exc).strip("'")
        return RedirectResponse(url=f"/?error={error}", status_code=303)
