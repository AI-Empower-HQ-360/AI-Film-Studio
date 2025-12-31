"""Service for synchronizing data between AI Film Studio and Salesforce CRM"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from .client import SalesforceClient
from .models import (
    ContactModel, 
    AIProjectModel, 
    AICreditModel, 
    YouTubeIntegrationModel,
    CreditTransactionModel
)

logger = logging.getLogger(__name__)


class SalesforceSyncService:
    """Service for syncing application data with Salesforce CRM"""
    
    def __init__(self):
        self.client = SalesforceClient()
    
    # ==================== Contact (User) Sync ====================
    
    def sync_user_to_contact(self, user_data: Dict[str, Any]) -> Optional[str]:
        """
        Sync user data to Salesforce Contact object.
        
        Args:
            user_data: Dictionary containing user information
                Required fields: user_id, email, last_name
                Optional fields: first_name, plan_type, credits
        
        Returns:
            Salesforce Contact ID if successful, None otherwise
        """
        try:
            # Extract user information
            user_id = user_data.get('user_id') or user_data.get('userId')
            email = user_data.get('email')
            
            # Split name if full name provided
            name = user_data.get('name', '')
            name_parts = name.split(' ', 1) if name else []
            first_name = user_data.get('first_name') or (name_parts[0] if len(name_parts) > 0 else None)
            last_name = user_data.get('last_name') or (name_parts[1] if len(name_parts) > 1 else 'User')
            
            # Build contact data
            contact_data = {
                'FirstName': first_name,
                'LastName': last_name,
                'Email': email,
                'Plan_Type__c': user_data.get('plan_type') or user_data.get('tier', 'free'),
                'Credits__c': user_data.get('credits', 0),
                'User_External_Id__c': user_id,
                'Last_Login__c': user_data.get('last_login_at', datetime.now(timezone.utc)).isoformat()
            }
            
            # Remove None values
            contact_data = {k: v for k, v in contact_data.items() if v is not None}
            
            # Upsert using external ID
            contact_id = self.client.upsert_record(
                sobject_type='Contact',
                external_id_field='User_External_Id__c',
                external_id=user_id,
                data=contact_data
            )
            
            if contact_id:
                logger.info(f"Synced user {user_id} to Salesforce Contact {contact_id}")
            
            return contact_id
            
        except Exception as e:
            logger.error(f"Error syncing user to Contact: {e}")
            return None
    
    # ==================== AI Project Sync ====================
    
    def sync_project_to_salesforce(self, project_data: Dict[str, Any]) -> Optional[str]:
        """
        Sync project data to Salesforce AI_Project__c custom object.
        
        Args:
            project_data: Dictionary containing project information
                Required fields: project_id, title, script, user_id, status
                Optional fields: duration, video_url, subtitles_url, thumbnail_url
        
        Returns:
            Salesforce AI_Project__c ID if successful, None otherwise
        """
        try:
            project_id = project_data.get('project_id') or project_data.get('projectId')
            user_id = project_data.get('user_id') or project_data.get('userId')
            
            # First, get the Salesforce Contact ID for this user
            contact = self.client.find_by_external_id('Contact', 'User_External_Id__c', user_id)
            if not contact:
                logger.warning(f"Contact not found for user {user_id}. Creating user first.")
                # Optionally create user if not exists
                return None
            
            contact_id = contact.get('Id')
            
            # Build project data
            project_sf_data = {
                'Name': project_data.get('title')[:80],  # Salesforce Name field usually has length limit
                'Script__c': project_data.get('script', ''),
                'Status__c': project_data.get('status', 'draft'),
                'Duration__c': project_data.get('duration'),
                'Video_URL__c': project_data.get('video_url') or project_data.get('outputUrl'),
                'Subtitles_URL__c': project_data.get('subtitles_url'),
                'Thumbnail_URL__c': project_data.get('thumbnail_url') or project_data.get('thumbnailUrl'),
                'Contact__c': contact_id,
                'Project_External_Id__c': project_id,
            }
            
            # Add completion date if completed
            if project_data.get('status') == 'completed' and project_data.get('completed_at'):
                project_sf_data['Completed_Date__c'] = project_data.get('completed_at')
            
            # Add error message if failed
            if project_data.get('status') == 'failed' and project_data.get('error_message'):
                project_sf_data['Error_Message__c'] = project_data.get('error_message')[:255]
            
            # Remove None values
            project_sf_data = {k: v for k, v in project_sf_data.items() if v is not None}
            
            # Upsert using external ID
            ai_project_id = self.client.upsert_record(
                sobject_type='AI_Project__c',
                external_id_field='Project_External_Id__c',
                external_id=project_id,
                data=project_sf_data
            )
            
            if ai_project_id:
                logger.info(f"Synced project {project_id} to Salesforce AI_Project__c {ai_project_id}")
            
            return ai_project_id
            
        except Exception as e:
            logger.error(f"Error syncing project to Salesforce: {e}")
            return None
    
    def update_project_status(self, project_id: str, status: str, **kwargs) -> bool:
        """
        Update project status in Salesforce.
        
        Args:
            project_id: Internal project ID
            status: New status value
            **kwargs: Additional fields to update (e.g., video_url, error_message)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find the Salesforce record
            record = self.client.find_by_external_id(
                'AI_Project__c',
                'Project_External_Id__c',
                project_id
            )
            
            if not record:
                logger.warning(f"AI_Project__c record not found for project {project_id}")
                return False
            
            sf_record_id = record.get('Id')
            
            # Build update data
            update_data = {'Status__c': status}
            
            if status == 'completed':
                update_data['Completed_Date__c'] = kwargs.get('completed_at', datetime.now(timezone.utc)).isoformat()
                if kwargs.get('video_url'):
                    update_data['Video_URL__c'] = kwargs['video_url']
            
            if status == 'failed' and kwargs.get('error_message'):
                update_data['Error_Message__c'] = kwargs['error_message'][:255]
            
            # Update the record
            success = self.client.update_record('AI_Project__c', sf_record_id, update_data)
            
            if success:
                logger.info(f"Updated AI_Project__c {sf_record_id} status to {status}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating project status in Salesforce: {e}")
            return False
    
    # ==================== Credit Sync ====================
    
    def sync_credit_record(self, credit_data: Dict[str, Any]) -> Optional[str]:
        """
        Sync credit/subscription data to Salesforce AI_Credit__c object.
        
        Args:
            credit_data: Dictionary containing credit information
                Required fields: user_id, plan_type, credits_allocated, reset_date
        
        Returns:
            Salesforce AI_Credit__c ID if successful, None otherwise
        """
        try:
            user_id = credit_data.get('user_id')
            
            # Get the Salesforce Contact ID
            contact = self.client.find_by_external_id('Contact', 'User_External_Id__c', user_id)
            if not contact:
                logger.warning(f"Contact not found for user {user_id}")
                return None
            
            contact_id = contact.get('Id')
            
            # Build credit data
            credits_allocated = credit_data.get('credits_allocated', 0)
            credits_used = credit_data.get('credits_used', 0)
            
            credit_sf_data = {
                'Name': f"{credit_data.get('plan_type', 'free').upper()} - {user_id[:8]}",
                'Contact__c': contact_id,
                'Plan_Type__c': credit_data.get('plan_type', 'free'),
                'Credits_Allocated__c': credits_allocated,
                'Credits_Used__c': credits_used,
                'Credits_Remaining__c': credits_allocated - credits_used,
                'Reset_Date__c': credit_data.get('reset_date').isoformat() if credit_data.get('reset_date') else None,
                'Expiry_Date__c': credit_data.get('expiry_date').isoformat() if credit_data.get('expiry_date') else None,
                'Status__c': credit_data.get('status', 'active')
            }
            
            # Remove None values
            credit_sf_data = {k: v for k, v in credit_sf_data.items() if v is not None}
            
            # Create new credit record
            credit_id = self.client.create_record('AI_Credit__c', credit_sf_data)
            
            if credit_id:
                logger.info(f"Created AI_Credit__c record {credit_id} for user {user_id}")
            
            return credit_id
            
        except Exception as e:
            logger.error(f"Error syncing credit record to Salesforce: {e}")
            return None
    
    def update_credit_usage(self, user_id: str, credits_used: int) -> bool:
        """
        Update credit usage for a user in Salesforce.
        
        Args:
            user_id: Internal user ID
            credits_used: Number of credits used
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find active credit record for user
            contact = self.client.find_by_external_id('Contact', 'User_External_Id__c', user_id)
            if not contact:
                logger.warning(f"Contact not found for user {user_id}")
                return False
            
            contact_id = contact.get('Id')
            
            # Query for active credit record
            soql = f"""
                SELECT Id, Credits_Allocated__c, Credits_Used__c 
                FROM AI_Credit__c 
                WHERE Contact__c = '{contact_id}' AND Status__c = 'active' 
                ORDER BY CreatedDate DESC 
                LIMIT 1
            """
            
            results = self.client.query(soql)
            if not results or results.get('totalSize', 0) == 0:
                logger.warning(f"No active credit record found for user {user_id}")
                return False
            
            credit_record = results['records'][0]
            sf_record_id = credit_record.get('Id')
            credits_allocated = credit_record.get('Credits_Allocated__c', 0)
            
            # Update credits
            update_data = {
                'Credits_Used__c': credits_used,
                'Credits_Remaining__c': credits_allocated - credits_used
            }
            
            success = self.client.update_record('AI_Credit__c', sf_record_id, update_data)
            
            if success:
                logger.info(f"Updated credit usage for user {user_id}")
                
                # Also update Contact credits
                self.client.update_record('Contact', contact_id, {'Credits__c': credits_allocated - credits_used})
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating credit usage in Salesforce: {e}")
            return False
    
    # ==================== YouTube Integration Sync ====================
    
    def sync_youtube_upload(self, youtube_data: Dict[str, Any]) -> Optional[str]:
        """
        Sync YouTube upload information to Salesforce YouTube_Integration__c object.
        
        Args:
            youtube_data: Dictionary containing YouTube upload information
                Required fields: project_id, channel_id, upload_status
                Optional fields: video_id, playlist_id, upload_date
        
        Returns:
            Salesforce YouTube_Integration__c ID if successful, None otherwise
        """
        try:
            project_id = youtube_data.get('project_id')
            
            # Find the AI_Project__c record
            project = self.client.find_by_external_id(
                'AI_Project__c',
                'Project_External_Id__c',
                project_id
            )
            
            if not project:
                logger.warning(f"AI_Project__c not found for project {project_id}")
                return None
            
            ai_project_id = project.get('Id')
            
            # Build YouTube integration data
            youtube_sf_data = {
                'Name': f"YouTube Upload - {project_id[:8]}",
                'AI_Project__c': ai_project_id,
                'Channel_Id__c': youtube_data.get('channel_id'),
                'Video_Id__c': youtube_data.get('video_id'),
                'Playlist_Id__c': youtube_data.get('playlist_id'),
                'Upload_Status__c': youtube_data.get('upload_status', 'pending'),
            }
            
            if youtube_data.get('upload_date'):
                youtube_sf_data['Upload_Date__c'] = youtube_data['upload_date'].isoformat()
            else:
                youtube_sf_data['Upload_Date__c'] = datetime.now(timezone.utc).isoformat()
            
            if youtube_data.get('error_message'):
                youtube_sf_data['Error_Message__c'] = youtube_data['error_message'][:255]
            
            # Remove None values
            youtube_sf_data = {k: v for k, v in youtube_sf_data.items() if v is not None}
            
            # Create YouTube integration record
            youtube_id = self.client.create_record('YouTube_Integration__c', youtube_sf_data)
            
            if youtube_id:
                logger.info(f"Created YouTube_Integration__c record {youtube_id} for project {project_id}")
            
            return youtube_id
            
        except Exception as e:
            logger.error(f"Error syncing YouTube upload to Salesforce: {e}")
            return None
    
    def update_youtube_upload_status(self, youtube_record_id: str, status: str, **kwargs) -> bool:
        """
        Update YouTube upload status in Salesforce.
        
        Args:
            youtube_record_id: Salesforce YouTube_Integration__c record ID
            status: New upload status
            **kwargs: Additional fields (video_id, error_message, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            update_data = {'Upload_Status__c': status}
            
            if status == 'completed':
                update_data['Upload_Date__c'] = kwargs.get('upload_date', datetime.now(timezone.utc)).isoformat()
                if kwargs.get('video_id'):
                    update_data['Video_Id__c'] = kwargs['video_id']
            
            if status == 'failed' and kwargs.get('error_message'):
                update_data['Error_Message__c'] = kwargs['error_message'][:255]
            
            success = self.client.update_record('YouTube_Integration__c', youtube_record_id, update_data)
            
            if success:
                logger.info(f"Updated YouTube_Integration__c {youtube_record_id} status to {status}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating YouTube upload status in Salesforce: {e}")
            return False
    
    # ==================== Task/Event Creation ====================
    
    def create_task_for_job_status(self, task_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a Salesforce Task to track AI job status or user notification.
        
        Args:
            task_data: Dictionary containing task information
                Required fields: subject, status, user_id
                Optional fields: description, priority, due_date
        
        Returns:
            Salesforce Task ID if successful, None otherwise
        """
        try:
            user_id = task_data.get('user_id')
            
            # Get Contact ID
            contact = self.client.find_by_external_id('Contact', 'User_External_Id__c', user_id)
            if not contact:
                logger.warning(f"Contact not found for user {user_id}")
                return None
            
            contact_id = contact.get('Id')
            
            # Build task data
            task_sf_data = {
                'Subject': task_data.get('subject', 'AI Job Status Update'),
                'Status': task_data.get('status', 'Not Started'),
                'Priority': task_data.get('priority', 'Normal'),
                'WhoId': contact_id,  # Link to Contact
                'Description': task_data.get('description', ''),
            }
            
            if task_data.get('due_date'):
                task_sf_data['ActivityDate'] = task_data['due_date'].isoformat()
            
            # Remove None values
            task_sf_data = {k: v for k, v in task_sf_data.items() if v is not None}
            
            # Create task
            task_id = self.client.create_record('Task', task_sf_data)
            
            if task_id:
                logger.info(f"Created Task {task_id} for user {user_id}")
            
            return task_id
            
        except Exception as e:
            logger.error(f"Error creating Task in Salesforce: {e}")
            return None
