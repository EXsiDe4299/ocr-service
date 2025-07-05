from fastapi import UploadFile, HTTPException
from starlette import status

from core.config import settings


def image_validation_dependency(image_file: UploadFile):
    if image_file.size > settings.ocr_image.max_image_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large",
        )
    if image_file.content_type.lower() not in settings.ocr_image.allowed_image_content_types: # fmt: skip
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid content type",
        )
    return image_file
