from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from app.models.user_old import UserOld

# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass

# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore

# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int | None = Field(default=None, foreign_key="userold.id", nullable=False)
    owner: "UserOld" = Relationship(back_populates="items")

# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int