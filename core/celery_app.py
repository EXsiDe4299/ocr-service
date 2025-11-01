from celery import Celery, current_app
from celery.signals import after_task_publish

from core.config import settings

celery_app = Celery(
    settings.celery.main,
    broker=str(settings.rabbitmq.url),
    backend=str(settings.redis.backend_url),
    include=["api.v1.tasks.ocr_tasks"],
    worker_concurrency=settings.celery.worker_concurrency,
    worker_prefetch_multiplier=settings.celery.worker_prefetch_multiplier,
    result_expires=settings.celery.result_expires,
)


@after_task_publish.connect(sender="api.v1.tasks.ocr_tasks.process_image")
def update_accepted_state(sender=None, headers=None, **kwargs):
    task = celery_app.tasks.get(sender)
    backend = task.backend if task else current_app
    backend.store_result(headers["id"], None, settings.celery.custom_states.ACCEPTED)
