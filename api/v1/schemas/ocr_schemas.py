from typing import Literal, Any

from pydantic import BaseModel


class UploadImageResponseScheme(BaseModel):
    task_id: str
    status: str | None = None
    message: str | None = None


class TaskResultResponseScheme(BaseModel):
    task_id: str
    state: Literal[
        "PENDING",
        "SUCCESS",
        "STARTED",
        "FAILURE",
    ]
    result: Any
