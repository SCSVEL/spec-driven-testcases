# Todo App — Built with Kiro Spec-Driven Development

This project demonstrates how to use [Kiro](https://kiro.dev)'s spec-driven approach to build a production-quality feature from scratch — with requirements, design, and implementation tasks all living alongside the code.

## What is Spec-Driven Development in Kiro?

Kiro introduces a structured workflow where you define _what_ to build before writing any code. A spec lives in `.kiro/specs/<feature>/` and consists of three documents that cascade into each other:

```
.kiro/specs/todo-app/
├── requirements.md   # User stories + acceptance criteria
├── design.md         # Architecture, data models, correctness properties
└── tasks.md          # Incremental implementation checklist
```

### The Workflow

**1. Requirements**
Write user stories and acceptance criteria in plain language. Each requirement is numbered and traceable. Example:

> Requirement 2.3: The Frontend SHALL display each task's title, description, reminder and completion status in the same row except description to next row.

**2. Design**
Kiro generates (or you author) a design doc that translates requirements into architecture decisions — component interfaces, data models, API contracts, and _correctness properties_. Properties are formal statements about system behaviour that map 1-to-1 to tests:

> Property 4: For any task returned by the API, the rendered DOM element should contain the task's title, description (if present), and completion status indicator. If `remind_at` is set, the reminder time SHALL be displayed in the same row as the title and controls.

**3. Tasks**
The design breaks down into an ordered, checkable implementation plan. Each task references the requirements it satisfies:

```markdown
- [x] 6.5 Implement PUT /tasks/{task_id} and DELETE /tasks/{task_id}
  - Raise HTTPException(404) for unknown IDs
  - On delete, call cancel_reminder(task_id)
  - _Requirements: 3.1, 3.2, 4.1, 4.2, 4.4_
```

**-----------------------------------------------------
Part of these tasks, we can emphasize the tests creation by specifying the
details, test techniques or edge cases in the steering docs; so Kiro use those as skills, and implement the tests.
Ex. Use playwright and create UI tests for end-to-end user scenarios
-----------------------------------------------------**

### Steering Files

`.kiro/steering/` holds always-on context that Kiro injects into every interaction — tech stack choices, project structure conventions, and product goals. This keeps the AI grounded in your project's decisions without repeating yourself.

```
.kiro/steering/
├── product.md    # What the app does and who it's for
├── tech.md       # Stack: FastAPI, SQLite, vanilla JS, APScheduler
└── structure.md  # File layout and coding conventions
```

---

## The App

A self-hosted browser-based task manager with a Python backend.

**Features:** add tasks · edit tasks · delete tasks · mark complete · set reminders

**Stack:** FastAPI + SQLite + APScheduler (backend) · HTML5 + vanilla JS (frontend)

## Getting Started

```bash
cd todo-app
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000

## Running Tests

```bash
cd todo-app
pytest
```

28 tests covering all API endpoints, validation, scheduler behaviour, and static file serving.

## Project Structure

```
todo-app/
├── main.py           # FastAPI routes
├── models.py         # Pydantic request/response models
├── database.py       # SQLite helpers
├── scheduler.py      # APScheduler reminder management
├── requirements.txt
├── static/
│   ├── index.html
│   ├── app.js
│   └── style.css
└── tests/
    ├── conftest.py
    ├── test_tasks_api.py
    └── test_scheduler.py
```

## How Requirements Drove the Code

When a requirement changed mid-build — for example, updating the task card layout so title, reminder, and controls share one row with description below — the cascade was:

1. Edit `requirements.md` (the source of truth)
2. Update `design.md` to reflect the new layout contract
3. Add a task in `tasks.md` (task 8.6)
4. Update `app.js` (`renderTask` restructured with a `task-top-row` div)
5. Update `style.css` (flex layout adjusted)

When a bug was found (reminder endpoint returning 422 due to naive vs timezone-aware datetime comparison), tests in `test_tasks_api.py` caught it and the fix was traced directly back to the validator in `models.py`.

This traceability — from user story → design property → test → code — is the core value of Kiro's spec-driven approach.
