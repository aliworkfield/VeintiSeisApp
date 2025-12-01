from typing import List, Optional
from sqlmodel import Session, select
from app.models.coupon import Coupon, CouponCreate, CouponUpdate
from app.models.user import User
from app.models.campaign import Campaign
from datetime import datetime

class CouponService:
    def __init__(self, session: Session):
        self.session = session

    def get_coupon(self, coupon_id: int) -> Optional[Coupon]:
        """Get a coupon by ID."""
        return self.session.get(Coupon, coupon_id)

    def get_coupons(self, skip: int = 0, limit: int = 100) -> List[Coupon]:
        """Get all coupons with pagination."""
        statement = select(Coupon).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_user_coupons(self, user_id: int) -> List[Coupon]:
        """Get all coupons assigned to a specific user."""
        statement = select(Coupon).where(Coupon.assigned_to_user == user_id)
        return self.session.exec(statement).all()

    def get_unassigned_coupons(self, skip: int = 0, limit: int = 100) -> List[Coupon]:
        """Get all unassigned coupons."""
        statement = select(Coupon).where(Coupon.assigned_to_user.is_(None)).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_available_coupons(self, skip: int = 0, limit: int = 100) -> List[Coupon]:
        """Get all available (unassigned and unredeemed) coupons."""
        statement = select(Coupon).where(
            Coupon.assigned_to_user.is_(None),
            Coupon.redeemed == False
        ).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_campaign_coupons(self, campaign_id: int, skip: int = 0, limit: int = 100) -> List[Coupon]:
        """Get all coupons for a specific campaign."""
        statement = select(Coupon).where(Coupon.campaign_id == campaign_id).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create_coupon(self, coupon_create: CouponCreate) -> Coupon:
        """Create a new coupon."""
        db_coupon = Coupon.model_validate(coupon_create)
        self.session.add(db_coupon)
        self.session.commit()
        self.session.refresh(db_coupon)
        return db_coupon

    def update_coupon(self, coupon_id: int, coupon_update: CouponUpdate) -> Optional[Coupon]:
        """Update an existing coupon."""
        db_coupon = self.get_coupon(coupon_id)
        if not db_coupon:
            return None
            
        coupon_data = coupon_update.dict(exclude_unset=True)
        for key, value in coupon_data.items():
            setattr(db_coupon, key, value)
            
        # Update the updated_at timestamp
        db_coupon.updated_at = datetime.utcnow()
        
        self.session.add(db_coupon)
        self.session.commit()
        self.session.refresh(db_coupon)
        return db_coupon

    def delete_coupon(self, coupon_id: int) -> bool:
        """Delete a coupon."""
        db_coupon = self.get_coupon(coupon_id)
        if not db_coupon:
            return False
            
        self.session.delete(db_coupon)
        self.session.commit()
        return True

    def redeem_coupon(self, coupon_id: int) -> Optional[Coupon]:
        """Redeem a coupon."""
        db_coupon = self.get_coupon(coupon_id)
        if not db_coupon:
            return None
            
        if db_coupon.redeemed:
            return db_coupon  # Already redeemed
            
        db_coupon.redeemed = True
        db_coupon.redeemed_at = datetime.utcnow()
        db_coupon.updated_at = datetime.utcnow()
        
        self.session.add(db_coupon)
        self.session.commit()
        self.session.refresh(db_coupon)
        return db_coupon

    def assign_coupon_to_user(self, coupon_id: int, user_id: int) -> Optional[Coupon]:
        """Assign a coupon to a user."""
        db_coupon = self.get_coupon(coupon_id)
        if not db_coupon:
            return None
            
        # Check if user exists
        user = self.session.get(User, user_id)
        if not user:
            return None
            
        db_coupon.assigned_to_user = user_id
        db_coupon.assigned_at = datetime.utcnow()
        db_coupon.updated_at = datetime.utcnow()
        
        self.session.add(db_coupon)
        self.session.commit()
        self.session.refresh(db_coupon)
        return db_coupon