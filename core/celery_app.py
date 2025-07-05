from celery import Celery

from core.config import settings

celery_app = Celery(
    settings.celery.main,
    broker=str(settings.celery.broker),
    backend=str(settings.celery.backend),
    include=["api.v1.tasks.ocr_tasks"],
    worker_concurrency=settings.celery.worker_concurrency,
    worker_prefetch_multiplier=settings.celery.worker_prefetch_multiplier,
    result_expires=settings.celery.result_expires,
)
