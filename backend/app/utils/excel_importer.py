import json
from typing import List, Dict, Any
import pandas as pd
from sqlmodel import Session, select
from app.models.coupon import CouponCreate
from app.models.campaign import CampaignCreate, Campaign
from app.services.campaign_service import CampaignService

class ExcelImporter:
    @staticmethod
    def import_coupons_from_excel(file_path: str, session: Session = None) -> List[CouponCreate]:
        """
        Import coupons from Excel file.
        
        Expected columns:
        - code (required)
        - campaign_name (optional, auto-create if not exists)
        - metadata (optional, JSON string)
        
        Business Rule: Required columns for Excel: code, campaign_name (auto-create if not exists)
        """
        df = pd.read_excel(file_path)
        
        # Dictionary to cache campaign IDs
        campaign_cache = {}
        
        coupons_data = []
        
        for _, row in df.iterrows():
            # Required field
            code = row['code']
            
            # Optional fields
            campaign_name = row.get('campaign_name')
            metadata_str = row.get('metadata', '{}')
            
            # Parse metadata if it's a string
            if isinstance(metadata_str, str):
                try:
                    metadata = json.loads(metadata_str)
                except json.JSONDecodeError:
                    metadata = {}
            else:
                metadata = metadata_str if metadata_str else {}
            
            # Handle campaign creation if campaign_name is provided
            campaign_id = None
            if campaign_name and session:
                # Check if campaign already exists in cache
                if campaign_name in campaign_cache:
                    campaign_id = campaign_cache[campaign_name]
                else:
                    # Check if campaign exists in database
                    statement = select(Campaign).where(Campaign.name == campaign_name)
                    existing_campaign = session.exec(statement).first()
                    
                    if existing_campaign:
                        campaign_id = existing_campaign.id
                        campaign_cache[campaign_name] = campaign_id
                    else:
                        # Create new campaign
                        campaign_service = CampaignService(session)
                        campaign_create = CampaignCreate(name=campaign_name)
                        new_campaign = campaign_service.create_campaign(campaign_create)
                        campaign_id = new_campaign.id
                        campaign_cache[campaign_name] = campaign_id
            
            coupon_data = {
                "code": code,
                "campaign_id": campaign_id,
                "metadata_": metadata
            }
            
            coupons_data.append(CouponCreate(**coupon_data))
            
        return coupons_data

    @staticmethod
    def import_coupons_from_json(file_path: str, session: Session = None) -> List[CouponCreate]:
        """
        Import coupons from JSON file.
        
        Expected format:
        [
            {
                "code": "COUPON_CODE",
                "campaign_name": "CAMPAIGN_NAME", (optional, auto-create if not exists)
                "metadata": { ... } (optional)
            },
            ...
        ]
        
        Business Rule: Required columns for Excel: code, campaign_name (auto-create if not exists)
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Dictionary to cache campaign IDs
        campaign_cache = {}
        
        coupons_data = []
        for item in data:
            # Handle campaign creation if campaign_name is provided
            campaign_id = None
            campaign_name = item.get("campaign_name")
            if campaign_name and session:
                # Check if campaign already exists in cache
                if campaign_name in campaign_cache:
                    campaign_id = campaign_cache[campaign_name]
                else:
                    # Check if campaign exists in database
                    statement = select(Campaign).where(Campaign.name == campaign_name)
                    existing_campaign = session.exec(statement).first()
                    
                    if existing_campaign:
                        campaign_id = existing_campaign.id
                        campaign_cache[campaign_name] = campaign_id
                    else:
                        # Create new campaign
                        campaign_service = CampaignService(session)
                        campaign_create = CampaignCreate(name=campaign_name)
                        new_campaign = campaign_service.create_campaign(campaign_create)
                        campaign_id = new_campaign.id
                        campaign_cache[campaign_name] = campaign_id
            
            coupon_data = {
                "code": item["code"],
                "campaign_id": campaign_id,
                "metadata_": item.get("metadata", {})
            }
            coupons_data.append(CouponCreate(**coupon_data))
            
        return coupons_data