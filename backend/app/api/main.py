from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, windows_auth, login_windows, auth
from app.core.config import settings

api_router = APIRouter()
# Include Windows auth router first to handle authentication
api_router.include_router(windows_auth.router)
api_router.include_router(login_windows.router, prefix="/login", tags=["windows-auth"])
api_router.include_router(auth.router)
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)