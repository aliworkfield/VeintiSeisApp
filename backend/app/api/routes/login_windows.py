from fastapi import APIRouter, Request, HTTPException
from datetime import timedelta

from app.core.windows_auth import get_windows_user, get_user_details
from app.core.security import create_access_token
from app.core.config import settings
from app import crud
from app.models import UserCreateOld as UserCreate
from app.core.db import engine
from sqlmodel import Session as SqlSession
import secrets
import logging
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

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

@router.get("/windows")
def login_with_windows(request: Request):
    """
    Windows login endpoint supporting both native and IIS modes.
    
    Returns Windows user information and JWT token.
    """
    username, mode = get_windows_user(request)
    if not username:
        raise HTTPException(status_code=401, detail="Unable to detect Windows user")

    logger.debug(f"Detected Windows user: {username}, mode: {mode}")

    # Convert Windows username to a valid email
    email = _windows_username_to_email(username)
    
    # Get additional user details if available
    user_details = get_user_details(username)
    
    try:
        # Create or get user in database
        with SqlSession(engine) as session:
            db_user = crud.get_user_by_email(session=session, email=email)
            
            if not db_user:
                logger.debug(f"User {email} not found, creating new user")
                # For Windows authentication, we don't need a real password
                # Create a user with a simple placeholder password that meets minimum requirements
                placeholder_password = "win12345"  # Simple 8-char placeholder
                user_in = UserCreate(
                    email=email,
                    password=placeholder_password,
                    full_name=user_details.get("full_name", username),
                    is_active=True
                )
                db_user = crud.create_windows_user(session=session, user_create=user_in)
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
            "token": token,
            "user": {
                "id": db_user.id,  # This is now an int, not a string
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