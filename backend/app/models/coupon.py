from typing import Optional, Dict, Any
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, JSON
from datetime import datetime

# Import models for forward reference resolution
from app.models.user import User
# Remove direct import of Campaign to avoid circular import
# from app.models.campaign import Campaign

class CouponBase(SQLModel):
    code: str = Field(unique=True, index=True, max_length=255)
    campaign_id: Optional[int] = Field(default=None, foreign_key="campaign.id")
    assigned_to_user: Optional[int] = Field(default=None, foreign_key="user.id")
    assigned_at: Optional[datetime] = None
    redeemed: bool = Field(default=False)
    redeemed_at: Optional[datetime] = None
    metadata_: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Coupon(CouponBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    assigned_user: Optional[User] = Relationship(back_populates="coupons")
    # Use string reference to avoid circular import
    campaign: Optional["Campaign"] = Relationship(back_populates="coupons")

class CouponCreate(CouponBase):
    pass

class CouponRead(CouponBase):
    id: int

class CouponUpdate(SQLModel):
    code: Optional[str] = None
    campaign_id: Optional[int] = None
    assigned_to_user: Optional[int] = None
    assigned_at: Optional[datetime] = None
    redeemed: Optional[bool] = None
    redeemed_at: Optional[datetime] = None
    metadata_: Optional[Dict[str, Any]] = None