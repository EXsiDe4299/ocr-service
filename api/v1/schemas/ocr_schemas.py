from typing import Any

from pydantic import BaseModel


class UploadImageResponseScheme(BaseModel):
    task_id: str
    status: str
    message: str


class TaskResultResponseScheme(BaseModel):
    task_id: str
    status: str | None = None
    message: str | None = None
    error: str | None = None
    result: Any | None = None
