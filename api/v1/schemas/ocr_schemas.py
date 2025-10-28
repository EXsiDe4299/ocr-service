from pydantic import BaseModel


class UploadImageResponseScheme(BaseModel):
    task_id: str
    status: str
    message: str


class TaskResultResponseScheme(BaseModel):
    task_id: str
    status: str
    message: str
    error: str | None = None
    result: str | None = None
