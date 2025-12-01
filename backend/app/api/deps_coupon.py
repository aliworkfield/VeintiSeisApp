from collections.abc import Generator
from typing import Annotated
import secrets

from fastapi import Depends, Header, HTTPException, status, Request
from sqlmodel import Session, select
from app.core.config import settings
from app.core.db import engine
from app.models import User, UserCreate
from app import crud
from app.core.security import verify_access_token
from app.core.windows_auth import get_windows_user, get_user_details

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_coupon_user_from_token(session: SessionDep, authorization: Annotated[str, Header()] = None) -> User:
    """Dependency that verifies a JWT token and returns the corresponding Coupon User."""
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
    
    # Check if user is active (we don't have an is_active field in the new model, so we assume active)
    # In a real implementation, you might want to add an is_active field to the User model
    
    return user


def get_coupon_user(session: SessionDep, 
                    request: Request,
                    token_user: Annotated[User, Depends(get_coupon_user_from_token)] = None) -> User:
    """Dependency that handles Windows authentication for coupon users or verifies JWT token.
    
    If a matching user doesn't exist in the DB, this will create a lightweight user record
    with appropriate roles so the rest of the application continues to work.
    """
    # First try Windows authentication
    username, mode = get_windows_user(request)
    if username:
        # Query by username field
        db_user = crud.get_coupon_user_by_username(session=session, username=username)
        
        if not db_user:
            # Create a new user for Windows authentication
            # Get additional user details if available
            user_details = get_user_details(username)
            
            # Map Windows user to roles (this is a simplified approach)
            roles = ["user"]  # Default role
            # In a real implementation, you might want to map specific users to admin roles
            
            # For Windows authentication, we don't need a real password
            # Create a user with a simple placeholder password that meets minimum requirements
            placeholder_password = "win12345"  # Simple 8-char placeholder
            
            user_in = UserCreate(
                username=username,
                password=placeholder_password,
                roles=roles,
                attributes={}  # Empty attributes by default
            )
            
            # Create the user with the coupon user creation function
            db_user = crud.create_coupon_windows_user(session=session, user_create=user_in)
        
        # Check if user is active (we assume all users are active in this model)
        return db_user
    
    # If Windows auth failed, try token authentication
    if token_user:
        return token_user
    
    # Not authenticated by either method
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing authentication credentials",
    )


CouponUser = Annotated[User, Depends(get_coupon_user)]