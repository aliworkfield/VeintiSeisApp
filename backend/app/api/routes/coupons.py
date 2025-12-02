from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
from typing import List, Optional
from app.api.deps_coupon import get_db, CouponUser
from app.core.roles_coupon import require_coupon_admin, require_coupon_manager, require_user
from app.services.coupon_service import CouponService
from app.services.campaign_service import CampaignService
from app.services.assignment_service import AssignmentService
from app.utils.excel_importer import ExcelImporter
from app.models.coupon import Coupon, CouponCreate, CouponUpdate, CouponRead
import json
import tempfile
import os

router = APIRouter(prefix="/coupons", tags=["coupons"])

@router.get("/me", response_model=List[CouponRead])
def read_my_coupons(
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Get coupons assigned to the current user.
    """
    coupon_service = CouponService(session)
    coupons = coupon_service.get_user_coupons(current_user.id)
    return coupons

@router.get("/unassigned", response_model=List[CouponRead])
def read_unassigned_coupons(
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Get all unassigned coupons (manager/admin only).
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    coupon_service = CouponService(session)
    coupons = coupon_service.get_unassigned_coupons()
    return coupons

@router.get("/available", response_model=List[CouponRead])
def read_available_coupons(
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Get all available coupons (manager/admin only).
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    coupon_service = CouponService(session)
    coupons = coupon_service.get_available_coupons()
    return coupons

@router.get("/all", response_model=List[CouponRead])
def read_all_coupons(
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Get all coupons (admin only).
    """
    # Check if user has required role
    require_coupon_admin(current_user)
    
    coupon_service = CouponService(session)
    coupons = coupon_service.get_coupons()
    return coupons

@router.get("/campaign/{campaign_id}", response_model=List[CouponRead])
def read_campaign_coupons(
    campaign_id: int,
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Get all coupons for a specific campaign (manager/admin only).
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    coupon_service = CouponService(session)
    coupons = coupon_service.get_campaign_coupons(campaign_id)
    return coupons

@router.post("/upload-excel", response_model=List[CouponRead])
async def upload_coupons_excel(
    current_user: CouponUser,
    session: Session = Depends(get_db),
    file: UploadFile = File(...)
):
    """
    Upload coupons from Excel file (manager/admin only).
    Business Rule: Accept Excel (.xlsx), Accept JSON array, Insert coupons with status unassigned,
    Required columns for Excel: code, campaign_name (auto-create if not exists)
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name

    try:
        # Import coupons from Excel
        coupons_data = ExcelImporter.import_coupons_from_excel(tmp_file_path, session)
        
        # Create coupons in database
        coupon_service = CouponService(session)
        created_coupons = []
        
        for coupon_data in coupons_data:
            created_coupon = coupon_service.create_coupon(coupon_data)
            created_coupons.append(created_coupon)
            
        return created_coupons
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@router.post("/upload-json", response_model=List[CouponRead])
async def upload_coupons_json(
    current_user: CouponUser,
    session: Session = Depends(get_db),
    file: UploadFile = File(...)
):
    """
    Upload coupons from JSON file (manager/admin only).
    Business Rule: Accept Excel (.xlsx), Accept JSON array, Insert coupons with status unassigned,
    Required columns for Excel: code, campaign_name (auto-create if not exists)
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name

    try:
        # Import coupons from JSON
        coupons_data = ExcelImporter.import_coupons_from_json(tmp_file_path, session)
        
        # Create coupons in database
        coupon_service = CouponService(session)
        created_coupons = []
        
        for coupon_data in coupons_data:
            created_coupon = coupon_service.create_coupon(coupon_data)
            created_coupons.append(created_coupon)
            
        return created_coupons
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@router.post("/assign", response_model=CouponRead)
def assign_coupon(
    coupon_id: int,
    user_id: int,
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Assign a coupon to a user (manager/admin only).
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    coupon_service = CouponService(session)
    assigned_coupon = coupon_service.assign_coupon_to_user(coupon_id, user_id)
    
    if not assigned_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found or assignment failed")
        
    return assigned_coupon

@router.post("/redeem", response_model=CouponRead)
def redeem_coupon(
    coupon_id: int,
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Redeem a coupon (user or admin).
    Regular users can only redeem their own coupons.
    Admins can redeem any coupon.
    """
    # Check if user has required role
    require_user(current_user)
    
    coupon_service = CouponService(session)
    
    # Check if user is admin or trying to redeem their own coupon
    if "coupon_admin" not in current_user.roles:
        # Regular user - check if coupon is assigned to them
        coupon = coupon_service.get_coupon(coupon_id)
        if not coupon or coupon.assigned_to_user != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot redeem coupon not assigned to you")
    
    redeemed_coupon = coupon_service.redeem_coupon(coupon_id)
    
    if not redeemed_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
        
    return redeemed_coupon

@router.delete("/{id}", response_model=bool)
def delete_coupon(
    id: int,
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Delete a coupon (admin only).
    """
    # Check if user has required role
    require_coupon_admin(current_user)
    
    coupon_service = CouponService(session)
    success = coupon_service.delete_coupon(id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Coupon not found")
        
    return success

@router.patch("/{id}", response_model=CouponRead)
def update_coupon(
    id: int,
    coupon_update: CouponUpdate,
    current_user: CouponUser,
    session: Session = Depends(get_db)
):
    """
    Update a coupon (manager/admin only).
    """
    # Check if user has required role
    require_coupon_manager(current_user)
    
    coupon_service = CouponService(session)
    updated_coupon = coupon_service.update_coupon(id, coupon_update)
    
    if not updated_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
        
    return updated_coupon