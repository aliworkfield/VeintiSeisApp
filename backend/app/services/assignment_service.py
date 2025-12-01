from typing import List, Optional
from sqlmodel import Session, select
from app.models.coupon import Coupon
from app.models.user import User
from app.models.campaign import Campaign
from datetime import datetime

class AssignmentService:
    def __init__(self, session: Session):
        self.session = session

    def assign_campaign_coupons_to_user(self, campaign_id: int, user_id: int) -> Optional[Coupon]:
        """Assign one unassigned coupon from a campaign to a user."""
        # Check if campaign exists
        campaign = self.session.get(Campaign, campaign_id)
        if not campaign:
            return None
            
        # Check if user exists
        user = self.session.get(User, user_id)
        if not user:
            return None

        # Find unassigned coupons belonging to that campaign
        statement = select(Coupon).where(
            Coupon.campaign_id == campaign_id,
            Coupon.assigned_to_user.is_(None)
        )
        
        unassigned_coupons = self.session.exec(statement).all()
        
        # Assign only one coupon per user (as per business rule)
        if unassigned_coupons:
            coupon_to_assign = unassigned_coupons[0]
            coupon_to_assign.assigned_to_user = user_id
            coupon_to_assign.assigned_at = datetime.utcnow()
            coupon_to_assign.updated_at = datetime.utcnow()
            
            self.session.add(coupon_to_assign)
            self.session.commit()
            self.session.refresh(coupon_to_assign)
            return coupon_to_assign
            
        return None

    def assign_coupons_to_users(self, campaign_id: int, user_ids: List[int]) -> List[Coupon]:
        """Assign coupons from a campaign to multiple users."""
        assigned_coupons = []
        
        for user_id in user_ids:
            assigned_coupon = self.assign_campaign_coupons_to_user(campaign_id, user_id)
            if assigned_coupon:
                assigned_coupons.append(assigned_coupon)
                
        return assigned_coupons