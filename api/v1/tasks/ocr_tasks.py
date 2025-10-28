import hashlib
import io

import pytesseract
from PIL import Image
from celery import Task, states

from core.celery_app import celery_app

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

    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="rus+eng")
    self.update_state(
        state=states.SUCCESS,
        meta={
            IMAGE_HASH_KEY: image_hash,
            FILENAME_KEY: filename,
            MESSAGE_KEY: "Image processed successfully",
            TEXT_KEY: text,
        },
    )
    return text
