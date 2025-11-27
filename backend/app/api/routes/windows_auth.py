from typing import Any

from fastapi import APIRouter

from app.api.deps import CurrentUser

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
