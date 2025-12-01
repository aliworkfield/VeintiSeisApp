import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Define the UpdatePassword model
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

# Shared properties for existing User model
class UserBaseOld(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    # Add Windows username field for backward compatibility
    windows_username: str | None = Field(default=None, max_length=255)

# Properties to receive via API on creation
class UserCreateOld(UserBaseOld):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class UserUpdateOld(UserBaseOld):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)

# Database model, database table inferred from class name
class UserOld(UserBaseOld, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")

# Properties to return via API, id is always required
class UserOutOld(UserBaseOld):
    id: int