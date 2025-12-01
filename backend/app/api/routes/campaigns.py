from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.deps_coupon import get_db, CouponUser
from app.core.roles_coupon import require_coupon_admin, require_user
from app.services.campaign_service import CampaignService
from app.services.assignment_service import AssignmentService
from app.models.campaign import Campaign, CampaignCreate, CampaignRead, CampaignUpdate
from app.models.coupon import Coupon, CouponRead

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.post("/", response_model=CampaignRead)
def create_campaign(
    *,
    session: Session = Depends(get_db),
    current_user: CouponUser = Depends(require_coupon_admin),
    campaign_in: CampaignCreate
):
    """
    Create new campaign (admin only).
    """
    campaign_service = CampaignService(session)
    campaign = campaign_service.create_campaign(campaign_in)
    return campaign

@router.get("/", response_model=List[CampaignRead])
def read_campaigns(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db),
    current_user: CouponUser = Depends(require_user)
):
    """
    Retrieve campaigns (all users).
    """
    campaign_service = CampaignService(session)
    campaigns = campaign_service.get_campaigns(skip=skip, limit=limit)
    return campaigns

@router.get("/{id}", response_model=CampaignRead)
def read_campaign(
    *,
    session: Session = Depends(get_db),
    current_user: CouponUser = Depends(require_user),
    id: int
):
    """
    Get campaign by ID (all users).
    """
    campaign_service = CampaignService(session)
    campaign = campaign_service.get_campaign(id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{id}", response_model=CampaignRead)
def update_campaign(
    *,
    session: Session = Depends(get_db),
    current_user: CouponUser = Depends(require_coupon_admin),
    id: int,
    campaign_in: CampaignUpdate
):
    """
    Update a campaign (admin only).
    """
    campaign_service = CampaignService(session)
    campaign = campaign_service.get_campaign(id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    updated_campaign = campaign_service.update_campaign(id, campaign_in)
    if not updated_campaign:
        raise HTTPException(status_code=400, detail="Campaign update failed")
    return updated_campaign

@router.delete("/{id}", response_model=bool)
def delete_campaign(
    *,
    session: Session = Depends(get_db),
    current_user: CouponUser = Depends(require_coupon_admin),
    id: int
):
    """
    Delete a campaign (admin only).
    """
    campaign_service = CampaignService(session)
    success = campaign_service.delete_campaign(id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return success

@router.post("/{campaign_id}/assign/{user_id}", response_model=CouponRead)
def assign_campaign_to_user(
    *,
    session: Session = Depends(get_db),
    current_user: CouponUser = Depends(require_coupon_admin),
    campaign_id: int,
    user_id: int
):
    """
    Assign one unassigned coupon from a campaign to a user (admin only).
    Business Rule: When manager assigns campaign "October_Lenovo" to a user:
    - find unassigned coupons belonging to that campaign
    - assign 1 coupon per user
    - set assigned_to_user + assigned_at
    """
    assignment_service = AssignmentService(session)
    assigned_coupon = assignment_service.assign_campaign_coupons_to_user(campaign_id, user_id)
    
    if not assigned_coupon:
        raise HTTPException(status_code=404, detail="Campaign or user not found, or no unassigned coupons available")
        
    return assigned_coupon