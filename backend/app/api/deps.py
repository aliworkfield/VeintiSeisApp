from collections.abc import Generator
from typing import Annotated
import secrets

from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session
from app.core.config import settings
from app.core.db import engine
from app.models import UserOld as User, UserCreateOld as UserCreate
from app import crud
from app.core.security import verify_access_token

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

def _windows_username_to_email(username: str) -> str:
    """Convert a Windows username (e.g. DOMAIN\\username) into a safe email-like string.

    This keeps compatibility with the existing `User.email` EmailStr field in the DB.
    """
    # normalize and replace characters that don't belong in an email local-part
    # If the incoming value already looks like an email, keep it as-is. This makes tests
    # and deployments flexible (tests often provide email addresses like FIRST_SUPERUSER).
    if "@" in username:
        return username

    cleaned = username.replace("\\", "_").replace("/", "_").replace(" ", "_")
    cleaned = cleaned.strip().lower()
    return f"{cleaned}@{settings.WINDOWS_EMAIL_DOMAIN}"


def _map_windows_username_to_role(username: str) -> str:
    """Map specific Windows usernames (exact match) into roles: 'admin' or 'user'.

    Admin users can be configured via the WINDOWS_ADMIN_USERS setting.
    """
    if not settings.WINDOWS_ADMIN_USERS:
        return "user"
    admin_list = [u.lower() for u in settings.WINDOWS_ADMIN_USERS]
    return "admin" if username.lower() in admin_list else "user"


def get_current_user_from_token(session: SessionDep, authorization: Annotated[str, Header()] = None) -> User:
    """Dependency that verifies a JWT token and returns the corresponding User."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.split("Bearer ")[1]
    payload = verify_access_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user = session.get(User, user_id)
    if not user:
        return None
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user


def get_current_user(session: SessionDep, 
                    x_windows_user: Annotated[str | None, Header(alias="X-Windows-User")] = None,
                    token_user: Annotated[User, Depends(get_current_user_from_token)] = None) -> User:
    """Dependency that reads the `X-Windows-User` header injected by IIS or verifies JWT token and returns a DB User.

    If a matching user doesn't exist in the DB, this will create a lightweight user record
    so the rest of the application (which expects User objects) continues to work.
    """
    # First try Windows authentication
    if x_windows_user:
        email = _windows_username_to_email(x_windows_user)
        user = crud.get_user_by_email(session=session, email=email)
        role = _map_windows_username_to_role(x_windows_user)

        if not user:
            # create a lightweight user in the DB so endpoints that rely on a User object keep working
            tmp_password = secrets.token_urlsafe(12)
            user_in = UserCreate(email=email, password=tmp_password, full_name=x_windows_user)
            # mark as superuser if mapped to admin
            if role == "admin":
                # UserCreate accepts is_superuser through UserBase defaults
                user_in.is_superuser = True  # type: ignore[attr-defined]
            user = crud.create_user(session=session, user_create=user_in)
        else:
            # keep DB-level is_superuser aligned with mapping
            should_be_admin = role == "admin"
            if user.is_superuser != should_be_admin:
                user.is_superuser = should_be_admin
                session.add(user)
                session.commit()
                session.refresh(user)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        return user
    
    # If Windows auth failed, try token authentication
    if token_user:
        return token_user
    
    # Not authenticated by either method
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing authentication credentials",
    )


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user