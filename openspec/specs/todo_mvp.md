# ToDo MVP Spec (Python app, OpenSpec-driven)

## Feature: Create task

### Scenario: Add task with valid title
Given the task list is empty
When the user submits a new task with title "Buy milk"
Then a new task is created
And the task title is "Buy milk"
And the task is marked as not completed
And the task appears in the task list

### Scenario: Reject empty title
Given the task list is empty
When the user submits a new task with an empty title
Then no task is created
And a validation error is shown saying "Title is required"

## Feature: List tasks

### Scenario: Show all tasks
Given tasks exist:
| id | title        | done  |
|----|--------------|-------|
| 1  | Buy milk     | false |
| 2  | Read a book  | true  |
When the user opens the home page
Then both tasks are displayed
And completed tasks are visually distinct from active tasks

## Feature: Complete task

### Scenario: Mark task as completed
Given a task exists with id 1 and title "Buy milk" and done false
When the user marks task 1 as completed
Then task 1 is updated with done true
And the home page shows task 1 as completed

### Scenario: Complete missing task id
Given no task exists with id 99
When the user marks task 99 as completed
Then no task is changed
And an error message is shown saying "Task not found"

## Feature: Dark mode

### Scenario: System dark mode is respected
Given the user's OS prefers dark color scheme
When the user opens the home page
Then the page background is dark
And text is light-colored

### Scenario: User can toggle dark mode manually
Given the user is on the home page
When the user clicks the "Toggle Dark Mode" button
Then the page switches to dark theme
And the preference is remembered on next visit (via localStorage)

### Scenario: User can toggle back to light mode
Given dark mode is currently active
When the user clicks the "Toggle Dark Mode" button
Then the page switches back to light theme

### Traceability to tests
- `test_dark_mode_toggle_button_present`
- `test_dark_mode_css_variables_present`
- `test_dark_mode_script_present`