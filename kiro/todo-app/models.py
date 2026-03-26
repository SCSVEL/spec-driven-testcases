from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class TaskCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator("title", mode="before")
    @classmethod
    def title_must_be_non_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be empty or whitespace")
        return stripped


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None

    @field_validator("title", mode="before")
    @classmethod
    def title_must_be_non_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("title must not be empty or whitespace")
        return stripped


class ReminderRequest(BaseModel):
    remind_at: datetime

    @field_validator("remind_at", mode="after")
    @classmethod
    def remind_at_must_be_future(cls, v: datetime) -> datetime:
        # Compare in UTC; treat naive datetimes as local time
        if v.tzinfo is None:
            v_aware = v.astimezone(timezone.utc)
        else:
            v_aware = v.astimezone(timezone.utc)
        if v_aware <= datetime.now(timezone.utc):
            raise ValueError("remind_at must be strictly in the future")
        return v


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    remind_at: datetime | None
