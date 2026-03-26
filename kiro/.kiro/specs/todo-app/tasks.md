# Implementation Plan: todo-app

## Overview

Incremental implementation of the FastAPI + SQLite backend and vanilla JS frontend. Each task builds on the previous, ending with full integration. Tests are co-located with the code they validate.

## Tasks

- [x] 1. Project scaffolding and dependencies
  - Create `requirements.txt` with `fastapi`, `uvicorn`, `apscheduler`, `hypothesis`, `pytest`, `httpx`
  - Create the `static/` directory with empty placeholder files (`index.html`, `app.js`, `style.css`)
  - Create `tests/conftest.py` with a `TestClient` fixture backed by an in-memory SQLite database
  - _Requirements: 7.1, 9.1, 9.2_

- [ ] 2. Data models (`models.py`)
  - [x] 2.1 Implement Pydantic models: `TaskCreate`, `TaskUpdate`, `ReminderRequest`, `TaskResponse`
    - Add `@field_validator` on `title` to strip whitespace and reject empty strings (HTTP 422)
    - Add `@field_validator` on `remind_at` to reject datetimes not strictly in the future (HTTP 422)
    - _Requirements: 1.2, 3.3, 6.2, 8.1, 8.2_

  - [ ]* 2.2 Write property test for serialisation round-trip (Property 16)
    - **Property 16: Task serialisation round-trip**
    - **Validates: Requirements 8.2, 8.3**
    - Place in `tests/test_serialisation.py`

  - [ ]* 2.3 Write property test for whitespace/empty title rejection (Property 2)
    - **Property 2: Empty/whitespace title is rejected on create and update**
    - **Validates: Requirements 1.2, 3.3**
    - Place in `tests/test_tasks_api.py`

  - [ ]* 2.4 Write property test for wrong-typed fields returning HTTP 422 (Property 17)
    - **Property 17: Wrong-typed fields return HTTP 422**
    - **Validates: Requirements 8.4**
    - Place in `tests/test_tasks_api.py`

- [ ] 3. Database layer (`database.py`)
  - [x] 3.1 Implement `init_db()` and schema creation (tasks table)
    - Use `sqlite3`; accept an optional connection parameter for test injection
    - _Requirements: 7.1, 7.2_

  - [x] 3.2 Implement `create_task()`, `get_all_tasks()`, `get_task()`, `update_task()`, `delete_task()`, `set_reminder()`
    - Return `dict` rows compatible with `TaskResponse`
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 6.1_

  - [ ]* 3.3 Write property test for database persistence across restarts (Property 14)
    - **Property 14: Database persistence across restarts**
    - **Validates: Requirements 7.1**
    - Place in `tests/test_database.py`

  - [ ]* 3.4 Write property test for idempotent schema initialisation (Property 15)
    - **Property 15: Schema initialisation is idempotent**
    - **Validates: Requirements 7.2**
    - Place in `tests/test_database.py`

- [ ] 4. Scheduler (`scheduler.py`)
  - [x] 4.1 Implement `start_scheduler()`, `schedule_reminder(task_id, remind_at, callback)`, `cancel_reminder(task_id)`
    - Use `APScheduler BackgroundScheduler`; keyed by `task_id`
    - `schedule_reminder` cancels any existing job for the same `task_id` before registering the new one
    - `cancel_reminder` is a no-op if no job exists
    - _Requirements: 6.1, 6.4, 6.5, 4.4_

  - [ ]* 4.2 Write unit tests for scheduler helpers
    - Mock `BackgroundScheduler`; verify `schedule_reminder` and `cancel_reminder` call correct methods
    - Test that updating a reminder replaces the old job (Property 13)
    - Test that `cancel_reminder` on a task with no job does not raise
    - Place in `tests/test_scheduler.py`
    - _Requirements: 4.4, 6.5_

- [x] 5. Checkpoint — core backend ready
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. FastAPI routes (`main.py`)
  - [x] 6.1 Set up FastAPI app: mount `StaticFiles` at `/static`, serve `index.html` at `GET /`
    - Call `init_db()` and `start_scheduler()` on startup
    - _Requirements: 9.1, 9.2_

  - [x] 6.2 Implement `GET /tasks` and `POST /tasks`
    - Delegate to `database.py` helpers; return `TaskResponse`
    - _Requirements: 1.1, 2.1_

  - [ ]* 6.3 Write property test for task creation round-trip (Property 1)
    - **Property 1: Task creation round-trip**
    - **Validates: Requirements 1.1**
    - Place in `tests/test_tasks_api.py`

  - [ ]* 6.4 Write property test for GET /tasks completeness (Property 3)
    - **Property 3: GET /tasks returns all persisted tasks**
    - **Validates: Requirements 2.1**
    - Place in `tests/test_tasks_api.py`

  - [x] 6.5 Implement `PUT /tasks/{task_id}` and `DELETE /tasks/{task_id}`
    - Raise `HTTPException(404)` for unknown IDs
    - On delete, call `cancel_reminder(task_id)`
    - _Requirements: 3.1, 3.2, 4.1, 4.2, 4.4_

  - [ ]* 6.6 Write property test for task update round-trip (Property 5)
    - **Property 5: Task update round-trip**
    - **Validates: Requirements 3.1**
    - Place in `tests/test_tasks_api.py`

  - [ ]* 6.7 Write property test for non-existent task ID returns 404 (Property 6)
    - **Property 6: Non-existent task ID returns HTTP 404**
    - **Validates: Requirements 3.2, 4.2, 6.3**
    - Place in `tests/test_tasks_api.py`

  - [ ]* 6.8 Write property test for delete removes task (Property 7)
    - **Property 7: Delete removes task from database**
    - **Validates: Requirements 4.1**
    - Place in `tests/test_tasks_api.py`

  - [ ]* 6.9 Write property test for delete cancels reminder (Property 8)
    - **Property 8: Deleting a task cancels its reminder job**
    - **Validates: Requirements 4.4**
    - Place in `tests/test_tasks_api.py`

  - [x] 6.10 Implement `POST /tasks/{task_id}/complete` and `POST /tasks/{task_id}/reminder`
    - `complete` toggles `completed` field; `reminder` validates future datetime, persists, and calls `schedule_reminder`
    - Raise `HTTPException(404)` for unknown IDs; raise `HTTPException(422)` for past datetimes
    - _Requirements: 5.1, 6.1, 6.2, 6.3, 6.5_

  - [ ]* 6.11 Write property test for completion toggle involution (Property 9)
    - **Property 9: Completion toggle is an involution**
    - **Validates: Requirements 5.1**
    - Place in `tests/test_tasks_api.py`

  - [ ]* 6.12 Write property test for reminder set round-trip (Property 11)
    - **Property 11: Reminder set round-trip**
    - **Validates: Requirements 6.1**
    - Place in `tests/test_reminders.py`

  - [ ]* 6.13 Write property test for past datetime rejection (Property 12)
    - **Property 12: Past/present datetime is rejected for reminders**
    - **Validates: Requirements 6.2**
    - Place in `tests/test_reminders.py`

  - [ ]* 6.14 Write property test for reminder replacement (Property 13)
    - **Property 13: Updating a reminder replaces the scheduler job**
    - **Validates: Requirements 6.5**
    - Place in `tests/test_reminders.py`

  - [ ]* 6.15 Write unit tests for static file serving and reminder callback
    - `GET /` returns `index.html` content
    - `GET /static/app.js` returns the JS file
    - Reminder callback logs expected message when triggered
    - Place in `tests/test_tasks_api.py`
    - _Requirements: 6.4, 9.1, 9.2_

- [x] 7. Checkpoint — API complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Frontend (`static/index.html`, `static/app.js`, `static/style.css`)
  - [x] 8.1 Build `index.html` with task form (title and description inputs only, submit button) and task list container
    - No reminder input in the creation form; reminder is only accessible via the edit form
    - _Requirements: 1.3_

  - [x] 8.2 Implement `app.js`: fetch and render all tasks on page load
    - Map each task to a DOM element showing title, description, and completion status
    - Display reminder time only if `remind_at` is set; omit the element entirely otherwise
    - Apply a `completed` CSS class to tasks where `completed === true`
    - _Requirements: 2.2, 2.3, 2.4, 5.3_

  - [ ] 8.6 Update task card layout so title, reminder, and controls share one row; description appears on the row below
    - Restructure `renderTask` in `app.js` to group title + reminder + buttons in a flex row, with description as a full-width element beneath
    - Update `style.css` to support the new layout (remove `flex: 1 1 100%` from `.task-title` and `.task-remind`; keep it on `.task-desc`)
    - _Requirements: 2.3_

  - [x] 8.3 Implement create, update, and delete task interactions in `app.js`
    - Create: POST on form submit (title + description only), append new task to list without reload
    - Delete: DELETE on button click, remove task element from DOM without reload
    - Update: Edit button opens an edit form with title, description, and reminder datetime inputs; PUT on submit, update DOM element in place; no inline editing
    - _Requirements: 1.4, 3.4, 3.5, 4.3_

  - [x] 8.4 Implement complete toggle in `app.js`; reminder is set only via the edit form
    - Checkbox/toggle sends `POST /tasks/{id}/complete`; update DOM class on response
    - Edit form includes a datetime input for reminder; on save, if reminder value present, also POST to `/tasks/{id}/reminder`; update displayed reminder time on the card
    - No standalone "Set Reminder" form on the task card
    - _Requirements: 5.2, 5.3, 3.4, 6.6_

  - [x] 8.5 Add `style.css`: minimal styles; `.completed` class applies strikethrough or distinct style
    - _Requirements: 5.3_

- [x] 9. Final checkpoint — full integration
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each property test maps 1-to-1 with a correctness property in the design document
- Use `TestClient` with in-memory SQLite for all API tests; mock `APScheduler` where needed
- Property tests use `hypothesis` with `@settings(max_examples=100)`
