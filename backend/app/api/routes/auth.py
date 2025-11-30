from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
import secrets
import uuid
import logging

from app.core.windows_auth import get_windows_user, get_user_details
from app.core.security import create_access_token
from app.core.config import settings
from app import crud
from app.models import UserCreate
from app.api.deps import get_db
from app.core.db import engine
from sqlmodel import Session as SqlSession

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/login", tags=["login"])

@router.get("/window")
def login_window(request: Request):
    """
    Windows login endpoint supporting both native and IIS modes.
    
    Returns Windows user information and JWT token.
    """
    username, mode = get_windows_user(request)
    if not username:
        raise HTTPException(401, "Unable to detect Windows user")

    logger.debug(f"Detected Windows user: {username}, mode: {mode}")

    # Get additional user details if available
    user_details = get_user_details(username)
    
    try:
        # Create or get user in database
        with SqlSession(engine) as session:
            db_user = crud.get_user_by_email(session=session, email=f"{username}@local.domain")
            
            if not db_user:
                logger.debug(f"User {username}@local.domain not found, creating new user")
                # Create a new user with a random password (at least 8 characters)
                tmp_password = secrets.token_urlsafe(8)  # This should be at least 8 characters
                user_in = UserCreate(
                    email=f"{username}@local.domain",
                    password=tmp_password,
                    full_name=user_details.get("full_name", username),
                    is_active=True
                )
                db_user = crud.create_user(session=session, user_create=user_in)
                logger.debug(f"Created new user with ID: {db_user.id}")
            else:
                logger.debug(f"Found existing user with ID: {db_user.id}")
            
            # Create JWT token using the actual user ID
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_access_token(
                subject=str(db_user.id), expires_delta=access_token_expires
            )
            logger.debug(f"Created JWT token for user ID: {db_user.id}")
        
        return {
            "windows_user": username,
            "auth_mode": mode,
            "token": token,
            "user": {
                "id": str(db_user.id),
                "email": db_user.email,
                "full_name": db_user.full_name,
                "is_active": db_user.is_active,
                "is_superuser": db_user.is_superuser
            }
        }
    except Exception as e:
        logger.error(f"Error creating authentication token: {str(e)}", exc_info=True)
        # If database operations fail, we can't create a proper token
        raise HTTPException(
            status_code=500,
            detail="Unable to create authentication token due to database error"
        )