from typing import Optional, Dict, Any
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, JSON
from datetime import datetime

# Define the UpdatePassword model
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

class UserBase(SQLModel):
    # Username in format DOMAIN\username for Windows authentication
    username: str = Field(unique=True, index=True, max_length=255)
    # Roles for authorization
    roles: list[str] = Field(default=["user"], sa_column=Column(JSON))  # Store as JSON
    # Extra permissions and attributes
    attributes: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))  # JSON field for extra permissions
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    coupons: list["Coupon"] = Relationship(back_populates="assigned_user")  # Forward reference
    # For Windows authentication, we still need a password field
    # This can be a placeholder for Windows authenticated users
    hashed_password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    roles: Optional[list[str]] = None
    attributes: Optional[Dict[str, Any]] = None