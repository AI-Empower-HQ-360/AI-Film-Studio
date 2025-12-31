"""Pydantic models for Salesforce CRM objects"""
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class ContactModel(BaseModel):
    """Salesforce Contact object (maps to Individual User)"""
    Id: Optional[str] = None
    FirstName: Optional[str] = None
    LastName: str
    Email: str
    Plan_Type__c: Literal["free", "pro", "enterprise"] = "free"
    Credits__c: int = 0
    User_External_Id__c: str  # Maps to our internal user ID
    Created_Date__c: Optional[datetime] = None
    Last_Login__c: Optional[datetime] = None


class AIProjectModel(BaseModel):
    """Salesforce AI_Project__c custom object"""
    Id: Optional[str] = None
    Name: str  # Project title
    Script__c: str  # Project script text
    Status__c: Literal["draft", "queued", "processing", "completed", "failed"] = "draft"
    Duration__c: Optional[int] = None  # Duration in seconds
    Video_URL__c: Optional[str] = None  # Final video URL
    Subtitles_URL__c: Optional[str] = None  # Subtitles URL
    Thumbnail_URL__c: Optional[str] = None
    Contact__c: Optional[str] = None  # FK to Contact
    Project_External_Id__c: str  # Maps to our internal project ID
    Created_Date__c: Optional[datetime] = None
    Completed_Date__c: Optional[datetime] = None
    Error_Message__c: Optional[str] = None


class AICreditModel(BaseModel):
    """Salesforce AI_Credit__c custom object (Credits/Subscription tracking)"""
    Id: Optional[str] = None
    Name: str  # Auto-generated
    Contact__c: str  # FK to Contact
    Plan_Type__c: Literal["free", "pro", "enterprise"] = "free"
    Credits_Allocated__c: int
    Credits_Used__c: int = 0
    Credits_Remaining__c: int
    Reset_Date__c: datetime
    Expiry_Date__c: Optional[datetime] = None
    Status__c: Literal["active", "expired", "cancelled"] = "active"


class YouTubeIntegrationModel(BaseModel):
    """Salesforce YouTube_Integration__c custom object"""
    Id: Optional[str] = None
    Name: str  # Auto-generated
    AI_Project__c: str  # FK to AI_Project__c
    Channel_Id__c: str
    Video_Id__c: Optional[str] = None
    Playlist_Id__c: Optional[str] = None
    Upload_Status__c: Literal["pending", "uploading", "completed", "failed"] = "pending"
    Upload_Date__c: Optional[datetime] = None
    Error_Message__c: Optional[str] = None


class CreditTransactionModel(BaseModel):
    """Model for tracking credit transactions (can be stored as Task/Event or custom object)"""
    transaction_id: str
    contact_id: str
    transaction_type: Literal["deduction", "purchase", "grant", "refund"]
    amount: int
    balance_after: int
    description: str
    created_at: datetime
