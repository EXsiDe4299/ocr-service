from fastapi import APIRouter

from api.v1.routers.ocr_router import ocr_router
from core.config import settings

v1_router = APIRouter(prefix=settings.v1_router.prefix)

v1_router.include_router(ocr_router)
