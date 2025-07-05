from typing import Literal

from pydantic import BaseModel


class UploadImageResponseScheme(BaseModel):
    filename: str
    task_id: str


class TaskResultResponseScheme(BaseModel):
    task_id: str
    state: Literal[
        "PENDING",
        "SUCCESS",
        "STARTED",
        "FAILURE",
    ]
    result: dict | None
