from fastapi import APIRouter

from api.v1.routers.v1_router import v1_router
from core.config import settings

api_router = APIRouter(prefix=settings.api_router.prefix)

api_router.include_router(v1_router)
