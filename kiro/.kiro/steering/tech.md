# Tech Stack

## Backend
- Python 3.11+
- FastAPI - REST API framework
- Uvicorn - ASGI server
- APScheduler - reminder/scheduling support
- SQLite - lightweight local database (via Python's built-in `sqlite3`)

## Frontend
- Plain HTML5 + vanilla JavaScript (no frameworks)
- CSS for styling (no preprocessors)
- Fetch API for communicating with the backend

## Package Manager
- pip with `requirements.txt`

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn main:app --reload

# Run tests
pytest
```
