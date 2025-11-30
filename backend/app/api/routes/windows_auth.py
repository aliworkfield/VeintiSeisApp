from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser
from app.core.windows_user import get_windows_user

router = APIRouter()

@router.get("/me", tags=["auth"])  # exposed at /api/v1/me
def read_me(current_user: CurrentUser) -> Any:
    """Return the logged-in user in the same shape as /users/me (UserPublic).

    Returning the same fields keeps the frontend compatible whether it calls
    /api/v1/users/me or /api/v1/me.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
    }

@router.get("/windows-user", tags=["auth"])
def read_windows_user(user: str = Depends(get_windows_user)) -> Any:
    """Return the Windows user authenticated by IIS.
    
    This endpoint demonstrates how to directly access the Windows user
    without going through the database user mapping.
    """
    return {
        "windows_user": user
    }