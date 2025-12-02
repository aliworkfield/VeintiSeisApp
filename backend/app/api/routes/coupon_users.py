from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.api.deps_coupon import SessionDep, CouponUser
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app import crud
from app.core.roles_coupon import require_coupon_admin

router = APIRouter(prefix="/coupon-users", tags=["coupon-users"])

@router.get("/", response_model=List[UserRead])
def read_users(
    *, 
    current_user: CouponUser,
    session: SessionDep
) -> Any:
    """
    Retrieve all coupon users (admin only).
    """
    # Check if user has required role
    require_coupon_admin(current_user)
    
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.get("/me", response_model=UserRead)
def read_user_me(current_user: CouponUser) -> Any:
    """
    Get current coupon user.
    """
    return current_user

@router.post("/", response_model=UserRead)
def create_user(
    *, 
    current_user: CouponUser,
    session: SessionDep, 
    user_in: UserCreate
) -> Any:
    """
    Create new coupon user (admin only).
    """
    # Check if user has required role
    require_coupon_admin(current_user)
    
    # Check if user already exists
    statement = select(User).where(User.username == user_in.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = crud.create_coupon_user(session=session, user_create=user_in)
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    *,
    current_user: CouponUser,
    session: SessionDep,
    user_id: int,
    user_in: UserUpdate
) -> Any:
    """
    Update a coupon user (admin only).
    """
    # Check if user has required role
    require_coupon_admin(current_user)
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    # Update user fields
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    *,
    current_user: CouponUser,
    session: SessionDep,
    user_id: int
) -> Any:
    """
    Delete a coupon user (admin only).
    """
    # Check if user has required role
    require_coupon_admin(current_user)
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}