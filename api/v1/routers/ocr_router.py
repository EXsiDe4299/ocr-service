import hashlib

from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, Depends
from redis.asyncio import Redis
from starlette import status

from api.v1.dependencies.ocr import image_validation_dependency
from api.v1.dependencies.redis_helper import redis_helper
from api.v1.schemas.ocr_schemas import (
    UploadImageResponseScheme,
    TaskResultResponseScheme,
)
from api.v1.tasks.ocr_tasks import process_image
from core.celery_app import celery_app
from core.config import settings

ocr_router = APIRouter(prefix=settings.ocr_router.prefix, tags=settings.ocr_router.tags)

# пока что используется только здесь, решил не выносить в конфиг
IMAGE_HASH_PREFIX = "image_hash:"


@ocr_router.post(
    settings.ocr_router.upload_image_endpoint_path,
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UploadImageResponseScheme,
)
async def upload_image_endpoint(
    image_file: UploadFile = Depends(image_validation_dependency),
    cache: Redis = Depends(redis_helper.get_redis),
):
    image_data = await image_file.read()

    # проверяем по хэшу изображения, не было ли оно обработано ранее
    image_hash = hashlib.md5(image_data).hexdigest()
    cached_task_id = await cache.get(IMAGE_HASH_PREFIX + image_hash)

    if cached_task_id is not None:
        accepted_task = AsyncResult(cached_task_id, app=celery_app)
        return UploadImageResponseScheme(
            task_id=cached_task_id,
            status=accepted_task.status,
            message="The image has been recently accepted",
        )

    task = process_image.delay(image_data)

    # записываем в кэш данные в формате {image_hash: task_id} во избежание повторной обработки одних и тех же изображений
    await cache.setex(
        name=IMAGE_HASH_PREFIX + image_hash,
        time=settings.celery.result_expires,
        value=task.id,
    )

    return UploadImageResponseScheme(
        task_id=task.id, status=task.status, message="Image processing started"
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
