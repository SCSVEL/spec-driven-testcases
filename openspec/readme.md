# OpenSpec Approach Used In This Project

This project follows a **spec-driven workflow**: we define behavior first, then write tests from that behavior, and only then implement code.

## 1) Spec First

We started in `specs/todo_mvp.md` and described features in plain language using Given/When/Then scenarios:

- Create task
- List tasks
- Complete task
- Dark mode

The spec acts as the source of truth for expected behavior.

## 2) Tests Derived From Spec

Before coding (or before finalizing code), we wrote tests that map to scenarios.

- Service-level behavior tests in `tests/test_todo_service.py`
- UI/HTTP behavior tests in `tests/test_routes.py`

Examples of scenario-to-test mapping:

- "Reject empty title" -> `test_reject_empty_title` and `test_post_task_empty_title_shows_error`
- "Complete missing task id" -> `test_complete_missing_task_id` and `test_complete_missing_task_shows_error`
- "Dark mode toggle" -> `test_dark_mode_toggle_button_present`, `test_dark_mode_css_variables_present`, `test_dark_mode_script_present`

This gives traceability from requirements to executable checks.

## 3) Minimal Implementation To Satisfy Tests

We implemented only what tests required:

- Domain/service logic in `app/service.py`
- FastAPI routes in `app/main.py`
- Server-rendered HTML/CSS/JS in `templates/index.html`

When behavior mismatches appeared (for example, 422 responses or template rendering issues), we fixed implementation and kept tests as the contract.

## 4) Edge Cases At Both Layers

We tested edge cases in both domain and UI layers:

- Empty/whitespace title
- Non-integer task IDs
- Missing task IDs
- Re-completing already completed task
- Empty-state rendering
- Dark mode presence/persistence hooks

This avoids false confidence from testing only business logic while missing route/template behavior.

## 5) Validate Frequently

We continuously ran tests with the project interpreter:

```bash
.\\.venv\\Scripts\\python.exe -m pytest tests/ -v
```

Current result after implementation: all tests passing.

## 6) Why This OpenSpec Workflow Helps

- Clear requirements before coding
- Better communication and reviewability
- Easier regression detection
- Faster iteration when adding new features

In short: **spec defines intent, tests enforce intent, code fulfills intent**.

## Practical Command Summary

Install dependencies:

```bash
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

Run tests:

```bash
.\\.venv\\Scripts\\python.exe -m pytest tests/ -v
```

Run app:

```bash
.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload
```
