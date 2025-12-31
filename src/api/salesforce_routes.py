"""API endpoints for Salesforce CRM integration and webhooks"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Header
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import logging

from src.services.salesforce import SalesforceSyncService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/salesforce", tags=["Salesforce CRM"])

# Initialize Salesforce sync service
salesforce_service = SalesforceSyncService()


# Request/Response Models
class UserSyncRequest(BaseModel):
    user_id: str
    email: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: str = "User"
    plan_type: str = "free"
    credits: int = 0


class ProjectSyncRequest(BaseModel):
    project_id: str
    user_id: str
    title: str
    script: str
    status: str = "draft"
    duration: Optional[int] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class ProjectStatusUpdate(BaseModel):
    project_id: str
    status: str
    video_url: Optional[str] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


class CreditUpdateRequest(BaseModel):
    user_id: str
    credits_used: int


class YouTubeUploadRequest(BaseModel):
    project_id: str
    channel_id: str
    video_id: Optional[str] = None
    playlist_id: Optional[str] = None
    upload_status: str = "pending"


class SalesforceWebhookPayload(BaseModel):
    """Generic webhook payload from Salesforce"""
    event_type: str
    object_type: str
    record_id: str
    data: Dict[str, Any]


# API Endpoints

@router.post("/sync/user")
async def sync_user(request: UserSyncRequest, background_tasks: BackgroundTasks):
    """
    Sync user data to Salesforce Contact object.
    This can be called when a user registers or updates their profile.
    """
    try:
        user_data = request.dict()
        
        # Run sync in background to avoid blocking
        def sync_task():
            contact_id = salesforce_service.sync_user_to_contact(user_data)
            if contact_id:
                logger.info(f"User {request.user_id} synced to Salesforce Contact {contact_id}")
        
        background_tasks.add_task(sync_task)
        
        return {
            "status": "success",
            "message": "User sync initiated",
            "user_id": request.user_id
        }
    except Exception as e:
        logger.error(f"Error initiating user sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/project")
async def sync_project(request: ProjectSyncRequest, background_tasks: BackgroundTasks):
    """
    Sync project data to Salesforce AI_Project__c custom object.
    This can be called when a project is created or updated.
    """
    try:
        project_data = request.dict()
        
        def sync_task():
            project_id = salesforce_service.sync_project_to_salesforce(project_data)
            if project_id:
                logger.info(f"Project {request.project_id} synced to Salesforce AI_Project__c {project_id}")
        
        background_tasks.add_task(sync_task)
        
        return {
            "status": "success",
            "message": "Project sync initiated",
            "project_id": request.project_id
        }
    except Exception as e:
        logger.error(f"Error initiating project sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/project-status")
async def update_project_status(request: ProjectStatusUpdate, background_tasks: BackgroundTasks):
    """
    Update project status in Salesforce.
    This should be called by the AI worker when job status changes.
    """
    try:
        def update_task():
            success = salesforce_service.update_project_status(
                project_id=request.project_id,
                status=request.status,
                video_url=request.video_url,
                error_message=request.error_message,
                completed_at=request.completed_at
            )
            if success:
                logger.info(f"Project {request.project_id} status updated to {request.status}")
        
        background_tasks.add_task(update_task)
        
        return {
            "status": "success",
            "message": "Project status update initiated",
            "project_id": request.project_id,
            "new_status": request.status
        }
    except Exception as e:
        logger.error(f"Error initiating project status update: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/credits")
async def update_credit_usage(request: CreditUpdateRequest, background_tasks: BackgroundTasks):
    """
    Update credit usage in Salesforce.
    This should be called when credits are deducted or added.
    """
    try:
        def update_task():
            success = salesforce_service.update_credit_usage(
                user_id=request.user_id,
                credits_used=request.credits_used
            )
            if success:
                logger.info(f"Credits updated for user {request.user_id}")
        
        background_tasks.add_task(update_task)
        
        return {
            "status": "success",
            "message": "Credit update initiated",
            "user_id": request.user_id
        }
    except Exception as e:
        logger.error(f"Error initiating credit update: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/youtube-upload")
async def sync_youtube_upload(request: YouTubeUploadRequest, background_tasks: BackgroundTasks):
    """
    Sync YouTube upload information to Salesforce.
    This should be called when a video is uploaded to YouTube.
    """
    try:
        youtube_data = request.dict()
        
        def sync_task():
            youtube_id = salesforce_service.sync_youtube_upload(youtube_data)
            if youtube_id:
                logger.info(f"YouTube upload synced to Salesforce: {youtube_id}")
        
        background_tasks.add_task(sync_task)
        
        return {
            "status": "success",
            "message": "YouTube upload sync initiated",
            "project_id": request.project_id
        }
    except Exception as e:
        logger.error(f"Error initiating YouTube upload sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def salesforce_webhook(
    payload: SalesforceWebhookPayload,
    x_salesforce_signature: Optional[str] = Header(None)
):
    """
    Webhook endpoint to receive updates from Salesforce.
    This can be used for bi-directional sync when Salesforce data changes.
    
    Note: In production, you should validate the webhook signature.
    """
    try:
        logger.info(f"Received Salesforce webhook: {payload.event_type} for {payload.object_type}")
        
        # TODO: Validate webhook signature
        # if x_salesforce_signature:
        #     validate_salesforce_signature(payload, x_salesforce_signature)
        
        # Handle different event types
        if payload.event_type == "created":
            logger.info(f"Record created in Salesforce: {payload.object_type} - {payload.record_id}")
        elif payload.event_type == "updated":
            logger.info(f"Record updated in Salesforce: {payload.object_type} - {payload.record_id}")
        elif payload.event_type == "deleted":
            logger.info(f"Record deleted in Salesforce: {payload.object_type} - {payload.record_id}")
        
        # Process the webhook data
        # This is where you would implement logic to update your local database
        # based on changes in Salesforce
        
        return {
            "status": "success",
            "message": "Webhook processed",
            "event_type": payload.event_type
        }
    except Exception as e:
        logger.error(f"Error processing Salesforce webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def salesforce_health():
    """
    Check Salesforce connection health.
    """
    try:
        is_connected = salesforce_service.client.is_connected()
        
        if not is_connected:
            # Try to connect
            is_connected = salesforce_service.client.connect()
        
        return {
            "status": "healthy" if is_connected else "disconnected",
            "connected": is_connected,
            "sync_enabled": salesforce_service.client._client is not None
        }
    except Exception as e:
        logger.error(f"Error checking Salesforce health: {e}")
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }
