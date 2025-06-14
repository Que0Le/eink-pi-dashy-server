from fastapi import APIRouter

from app.api.routes import images, states
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(images.router)
api_router.include_router(states.router)
# api_router.include_router(utils.router)
# api_router.include_router(items.router)


# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
