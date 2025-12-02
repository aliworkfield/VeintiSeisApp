import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
# Import all models directly from their source files
from app.models.item import Item, ItemCreate
from app.models.user import User, UserCreate
from app.models.user_old import UserOld, UserCreateOld, UserUpdateOld, UpdatePassword
from app.models.other import Message, Token, TokenPayload, NewPassword

def create_user(*, session: Session, user_create: UserCreateOld) -> UserOld:
    db_obj = UserOld.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_windows_user(*, session: Session, user_create: UserCreateOld) -> UserOld:
    """Create a user for Windows authentication without hashing the password.
    
    For Windows-authenticated users, we don't need to hash passwords since authentication
    is handled by Windows. We still need to provide a password to satisfy the model
    requirements, but it won't be used for authentication.
    """
    # Create a simple placeholder hashed password
    placeholder_hash = "$2b$12$CCCCCCCCCCCCCCCCCCCCC.E5YPO9kmyZVxF2pUU58uVz8I70MuB.U6"  # bcrypt hash of "placeholder"
    db_obj = UserOld.model_validate(
        user_create, update={"hashed_password": placeholder_hash}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_coupon_user(*, session: Session, user_create: UserCreate) -> User:
    """Create a new coupon user."""
    # For coupon users, we'll hash the password normally
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_coupon_windows_user(*, session: Session, user_create: UserCreate) -> User:
    """Create a user for Windows authentication without hashing the password.
    
    For Windows-authenticated users, we don't need to hash passwords since authentication
    is handled by Windows. We still need to provide a password to satisfy the model
    requirements, but it won't be used for authentication.
    """
    # Create a simple placeholder hashed password
    placeholder_hash = "$2b$12$CCCCCCCCCCCCCCCCCCCCC.E5YPO9kmyZVxF2pUU58uVz8I70MuB.U6"  # bcrypt hash of "placeholder"
    db_obj = User.model_validate(
        user_create, update={"hashed_password": placeholder_hash}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_user(*, session: Session, db_user: UserOld, user_in: UserUpdateOld) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_coupon_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(*, session: Session, email: str) -> UserOld | None:
    statement = select(UserOld).where(UserOld.email == email)
    session_user = session.exec(statement).first()
    return session_user

def get_coupon_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> UserOld | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_item(*, session: Session, item_in: ItemCreate, owner_id: int) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item