# Project Structure

```
todo-app/
├── main.py              # FastAPI app entry point, route definitions
├── models.py            # Data models (Pydantic + DB schema)
├── database.py          # SQLite connection and helpers
├── scheduler.py         # Reminder scheduling logic (APScheduler)
├── requirements.txt     # Python dependencies
└── static/
    ├── index.html       # Main UI
    ├── app.js           # Frontend logic (Fetch API calls)
    └── style.css        # Styles
```

## Conventions
- All API routes live in `main.py`; split into separate routers if the file grows large
- Frontend communicates with the backend exclusively via the REST API
- Static files are served directly by FastAPI using `StaticFiles`
- Keep business logic out of route handlers — use helper functions in dedicated modules
