import io

import pytesseract
from PIL import Image

from core.celery_app import celery_app


@celery_app.task()
def process_image(image_data: bytes):
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="rus+eng")
    return text.strip()
