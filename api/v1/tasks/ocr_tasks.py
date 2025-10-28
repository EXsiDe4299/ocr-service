import hashlib
import io

import pytesseract
from PIL import Image
from celery import Task, states
from redis import Redis

from core.celery_app import celery_app
from core.config import settings

redis_client = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    decode_responses=settings.redis.decode_responses,
)

IMAGE_HASH_KEY = "image_hash"
FILENAME_KEY = "filename"
MESSAGE_KEY = "message"
TEXT_KEY = "text"


@celery_app.task(bind=True)
def process_image(self: Task, filename: str, image_data: bytes):
    image_hash = hashlib.md5(image_data).hexdigest()
    self.update_state(
        state=states.STARTED,
        meta={
            IMAGE_HASH_KEY: image_hash,
            FILENAME_KEY: filename,
            MESSAGE_KEY: "Processing image...",
        },
    )

    cached_result = redis_client.get(image_hash)
    if cached_result is not None:
        self.update_state(
            state=states.SUCCESS,
            meta={
                IMAGE_HASH_KEY: image_hash,
                FILENAME_KEY: filename,
                MESSAGE_KEY: "Result from cache",
                TEXT_KEY: cached_result,
            },
        )
        return cached_result

    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="rus+eng")

    redis_client.set(image_hash, text)
    redis_client.expire(image_hash, 3600)
    self.update_state(
        state=states.SUCCESS,
        meta={
            IMAGE_HASH_KEY: image_hash,
            FILENAME_KEY: filename,
            MESSAGE_KEY: "Image processed and cached",
            TEXT_KEY: text,
        },
    )
    return text
