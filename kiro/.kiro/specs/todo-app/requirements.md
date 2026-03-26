# Requirements Document

## Introduction

A browser-based ToDo application that allows individual users to manage daily tasks through a clean, minimal UI. The frontend is served as static HTML/JS/CSS by a Python FastAPI backend, which persists tasks in a local SQLite database and supports scheduled reminders via APScheduler.

## Glossary

- **API**: The FastAPI REST interface exposed by the backend at defined HTTP endpoints.
- **App**: The FastAPI backend application defined in `main.py`.
- **Database**: The SQLite database managed through `database.py`.
- **Frontend**: The browser-based UI composed of `index.html`, `app.js`, and `style.css`.
- **Reminder**: A scheduled notification associated with a task, triggered at a user-specified date and time.
- **Scheduler**: The APScheduler-based component in `scheduler.py` responsible for managing reminder jobs.
- **Task**: A user-created item with a title, optional description, completion status, and optional reminder time.

---

## Requirements

### Requirement 1: Create a Task

**User Story:** As a user, I want to add a new task, so that I can track something I need to do.

#### Acceptance Criteria

1. WHEN a user submits a task creation request with a non-empty title, THE API SHALL persist the task in the Database and return the created task with a unique integer ID, title, description, completion status of `false`, and reminder time.
2. IF a task creation request is submitted with an empty or missing title, THEN THE API SHALL return an HTTP 422 response with a descriptive validation error.
3. THE Frontend SHALL provide an input form that allows the user to enter a task title and an optional description, and submit the form to create a task.
4. WHEN a task is successfully created, THE Frontend SHALL display the new task in the task list without requiring a full page reload.
5. WHEN a task has a reminder time set, THE Frontend SHALL display the reminder time alongside the task in the task list.

---

### Requirement 2: Read / List Tasks

**User Story:** As a user, I want to see all my tasks, so that I can review what needs to be done.

#### Acceptance Criteria

1. THE API SHALL expose a GET endpoint that returns all tasks stored in the Database as a JSON array.
2. WHEN the Frontend loads, THE Frontend SHALL fetch and display all existing tasks from the API.
3. THE Frontend SHALL display each task's title, description, reminder and completion status in same row except descirption to next row.
4. IF a task has a reminder time set, THE Frontend SHALL display the reminder time alongside the task; otherwise no reminder time SHALL be shown.

---

### Requirement 3: Update a Task

**User Story:** As a user, I want to edit an existing task, so that I can correct or update its details.

#### Acceptance Criteria

1. WHEN a user submits an update request for an existing task ID with valid fields, THE API SHALL update the corresponding task in the Database and return the updated task.
2. IF an update request references a task ID that does not exist in the Database, THEN THE API SHALL return an HTTP 404 response with a descriptive error message.
3. IF an update request provides an empty title, THEN THE API SHALL return an HTTP 422 response with a descriptive validation error.
4. THE Frontend SHALL allow the user to edit a task's title, description, and reminder time exclusively through an Edit button that opens an edit form; inline editing SHALL NOT be supported.
5. THE Frontend SHALL NOT display a persistent "Set Reminder" control on each task in the task list; reminder editing SHALL only be accessible via the edit form.

---

### Requirement 4: Delete a Task

**User Story:** As a user, I want to delete a task, so that I can remove items I no longer need.

#### Acceptance Criteria

1. WHEN a user submits a delete request for an existing task ID, THE API SHALL remove the task from the Database and return an HTTP 200 response confirming deletion.
2. IF a delete request references a task ID that does not exist in the Database, THEN THE API SHALL return an HTTP 404 response with a descriptive error message.
3. WHEN a task is successfully deleted, THE Frontend SHALL remove the task from the task list without requiring a full page reload.
4. WHEN a task with an active Reminder is deleted, THE Scheduler SHALL cancel the associated reminder job.

---

### Requirement 5: Mark a Task as Complete

**User Story:** As a user, I want to mark a task as complete, so that I can track my progress.

#### Acceptance Criteria

1. WHEN a user submits a completion toggle request for an existing task ID, THE API SHALL update the task's completion status in the Database and return the updated task.
2. THE Frontend SHALL provide a checkbox or toggle control for each task that sends the completion toggle request to the API when activated.
3. WHEN a task is marked complete, THE Frontend SHALL visually distinguish it from incomplete tasks (e.g., strikethrough text or a distinct style).

---

### Requirement 6: Set a Reminder

**User Story:** As a user, I want to set a reminder on a task, so that I am notified at a specific time.

#### Acceptance Criteria

1. WHEN a user submits a request to set a reminder on an existing task with a valid future datetime, THE API SHALL persist the reminder time on the task and instruct THE Scheduler to register a one-time job for that datetime.
2. IF a reminder request specifies a datetime that is not in the future, THEN THE API SHALL return an HTTP 422 response with a descriptive validation error.
3. IF a reminder request references a task ID that does not exist in the Database, THEN THE API SHALL return an HTTP 404 response with a descriptive error message.
4. WHEN the scheduled reminder time is reached, THE Scheduler SHALL execute the reminder action (e.g., log the reminder or invoke a notification callback).
5. WHEN a reminder is updated to a new future datetime, THE Scheduler SHALL cancel the previous job and register a new job for the updated datetime.
6. THE Frontend SHALL provide a datetime input inside the edit form that allows the user to set or update a reminder time and submit it to the API.

---

### Requirement 7: Data Persistence

**User Story:** As a user, I want my tasks to be saved between sessions, so that I do not lose my data when I close the browser.

#### Acceptance Criteria

1. THE Database SHALL persist all tasks to a SQLite file on disk so that data survives application restarts.
2. WHEN the App starts, THE Database SHALL initialise the required schema if it does not already exist, without destroying existing data.

---

### Requirement 8: API Data Validation and Serialisation

**User Story:** As a developer, I want all API inputs and outputs to be validated and consistently serialised, so that the system remains reliable and predictable.

#### Acceptance Criteria

1. THE API SHALL validate all incoming request bodies using Pydantic models defined in `models.py`.
2. THE API SHALL serialise all responses as JSON conforming to the Pydantic response models.
3. FOR ALL valid Task objects, serialising a Task to JSON and then deserialising the JSON SHALL produce an equivalent Task object (round-trip property).
4. IF a request body contains fields of an incorrect type, THEN THE API SHALL return an HTTP 422 response with field-level error details.

---

### Requirement 9: Static Frontend Serving

**User Story:** As a user, I want to access the application through a web browser without a separate deployment step, so that setup is simple.

#### Acceptance Criteria

1. THE App SHALL serve the contents of the `static/` directory as static files accessible at the `/static` path prefix.
2. THE App SHALL serve `static/index.html` as the root response when a browser requests `/`.
