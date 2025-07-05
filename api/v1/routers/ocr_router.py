from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, Depends
from starlette import status

from api.v1.dependencies.ocr import image_validation_dependency
from api.v1.schemas.ocr_schemas import (
    UploadImageResponseScheme,
    TaskResultResponseScheme,
)
from api.v1.tasks.ocr_tasks import process_image
from core.celery_app import celery_app
from core.config import settings

ocr_router = APIRouter(prefix=settings.ocr_router.prefix, tags=settings.ocr_router.tags)


@ocr_router.post(
    settings.ocr_router.upload_image_endpoint_path,
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UploadImageResponseScheme,
)
async def upload_image_endpoint(
    image_file: UploadFile = Depends(image_validation_dependency),
):
    image_data = await image_file.read()
    task = process_image.delay(image_file.filename, image_data)
    return UploadImageResponseScheme(
        filename=image_file.filename,
        task_id=task.id,
    )


@ocr_router.get(
    settings.ocr_router.get_task_endpoint_path,
    status_code=status.HTTP_200_OK,
    response_model=TaskResultResponseScheme,
)
async def get_task_endpoint(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    result = TaskResultResponseScheme(
        task_id=task_id,
        state=task_result.state,
        result=task_result.result,
    )
    return result
