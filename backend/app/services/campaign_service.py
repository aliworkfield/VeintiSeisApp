from typing import List, Optional
from sqlmodel import Session, select
from app.models.campaign import Campaign, CampaignCreate, CampaignUpdate

class CampaignService:
    def __init__(self, session: Session):
        self.session = session

    def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        """Get a campaign by ID."""
        return self.session.get(Campaign, campaign_id)

    def get_campaigns(self, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get all campaigns with pagination."""
        statement = select(Campaign).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create_campaign(self, campaign_create: CampaignCreate) -> Campaign:
        """Create a new campaign."""
        db_campaign = Campaign.model_validate(campaign_create)
        self.session.add(db_campaign)
        self.session.commit()
        self.session.refresh(db_campaign)
        return db_campaign

    def update_campaign(self, campaign_id: int, campaign_update: CampaignUpdate) -> Optional[Campaign]:
        """Update an existing campaign."""
        db_campaign = self.get_campaign(campaign_id)
        if not db_campaign:
            return None
            
        campaign_data = campaign_update.dict(exclude_unset=True)
        for key, value in campaign_data.items():
            setattr(db_campaign, key, value)
            
        self.session.add(db_campaign)
        self.session.commit()
        self.session.refresh(db_campaign)
        return db_campaign

    def delete_campaign(self, campaign_id: int) -> bool:
        """Delete a campaign."""
        db_campaign = self.get_campaign(campaign_id)
        if not db_campaign:
            return False
            
        self.session.delete(db_campaign)
        self.session.commit()
        return True