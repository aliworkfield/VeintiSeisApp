from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# Import models for forward reference resolution
from app.models.coupon import Coupon

class CampaignBase(SQLModel):
    name: str = Field(max_length=255)
    description: Optional[str] = None
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Campaign(CampaignBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    coupons: List[Coupon] = Relationship(back_populates="campaign")

class CampaignCreate(CampaignBase):
    pass

class CampaignRead(CampaignBase):
    id: int

class CampaignUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None