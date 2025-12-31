"""Tests for Salesforce CRM integration"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.services.salesforce import SalesforceClient, SalesforceSyncService
from src.services.salesforce.models import (
    ContactModel,
    AIProjectModel,
    AICreditModel,
    YouTubeIntegrationModel
)


@pytest.fixture
def mock_salesforce_client():
    """Mock Salesforce client for testing"""
    with patch('src.services.salesforce.client.Salesforce') as mock_sf:
        mock_instance = Mock()
        mock_sf.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def salesforce_client(mock_salesforce_client):
    """Create SalesforceClient instance with mocked connection"""
    client = SalesforceClient()
    client._client = mock_salesforce_client
    client._connected = True
    return client


@pytest.fixture
def sync_service(salesforce_client):
    """Create SalesforceSyncService with mocked client"""
    service = SalesforceSyncService()
    service.client = salesforce_client
    return service


class TestSalesforceClient:
    """Test SalesforceClient class"""
    
    def test_connect_success(self, mock_salesforce_client):
        """Test successful connection to Salesforce"""
        with patch('src.config.settings.SALESFORCE_SYNC_ENABLED', True):
            with patch('src.config.settings.SALESFORCE_USERNAME', 'test@example.com'):
                with patch('src.config.settings.SALESFORCE_PASSWORD', 'password'):
                    with patch('src.config.settings.SALESFORCE_SECURITY_TOKEN', 'token'):
                        client = SalesforceClient()
                        result = client.connect()
                        
                        assert result is True
                        assert client.is_connected() is True
    
    def test_connect_disabled(self):
        """Test connection when sync is disabled"""
        with patch('src.config.settings.SALESFORCE_SYNC_ENABLED', False):
            client = SalesforceClient()
            result = client.connect()
            
            assert result is False
            assert client.is_connected() is False
    
    def test_create_record_success(self, salesforce_client):
        """Test creating a record in Salesforce"""
        mock_contact = Mock()
        mock_contact.create.return_value = {'success': True, 'id': 'test_id_123'}
        salesforce_client.Contact = mock_contact
        
        data = {'FirstName': 'John', 'LastName': 'Doe', 'Email': 'john@example.com'}
        record_id = salesforce_client.create_record('Contact', data)
        
        assert record_id == 'test_id_123'
        mock_contact.create.assert_called_once_with(data)
    
    def test_create_record_failure(self, salesforce_client):
        """Test failed record creation"""
        mock_contact = Mock()
        mock_contact.create.return_value = {'success': False, 'errors': ['Error message']}
        salesforce_client.Contact = mock_contact
        
        data = {'FirstName': 'John'}
        record_id = salesforce_client.create_record('Contact', data)
        
        assert record_id is None
    
    def test_update_record_success(self, salesforce_client):
        """Test updating a record"""
        mock_contact = Mock()
        mock_contact.update.return_value = None  # Update returns 204 No Content
        salesforce_client.Contact = mock_contact
        
        data = {'Email': 'newemail@example.com'}
        result = salesforce_client.update_record('Contact', 'test_id_123', data)
        
        assert result is True
        mock_contact.update.assert_called_once_with('test_id_123', data)
    
    def test_get_record_success(self, salesforce_client):
        """Test retrieving a record"""
        mock_contact = Mock()
        mock_contact.get.return_value = {'Id': 'test_id_123', 'Email': 'john@example.com'}
        salesforce_client.Contact = mock_contact
        
        record = salesforce_client.get_record('Contact', 'test_id_123')
        
        assert record is not None
        assert record['Id'] == 'test_id_123'
        assert record['Email'] == 'john@example.com'
    
    def test_query_success(self, salesforce_client):
        """Test SOQL query execution"""
        salesforce_client.query.return_value = {
            'totalSize': 1,
            'records': [{'Id': 'test_id_123', 'Name': 'Test'}]
        }
        
        results = salesforce_client.query("SELECT Id, Name FROM Contact WHERE Email = 'test@example.com'")
        
        assert results is not None
        assert results['totalSize'] == 1
        assert len(results['records']) == 1
    
    def test_find_by_external_id(self, salesforce_client):
        """Test finding record by external ID"""
        salesforce_client.query = Mock(return_value={
            'totalSize': 1,
            'records': [{'Id': 'sf_id_123'}]
        })
        
        record = salesforce_client.find_by_external_id(
            'Contact',
            'User_External_Id__c',
            'user_123'
        )
        
        assert record is not None
        assert record['Id'] == 'sf_id_123'


class TestSalesforceSyncService:
    """Test SalesforceSyncService class"""
    
    def test_sync_user_to_contact_success(self, sync_service):
        """Test syncing user to Salesforce Contact"""
        user_data = {
            'user_id': 'user_123',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'plan_type': 'pro',
            'credits': 30
        }
        
        sync_service.client.upsert_record = Mock(return_value='contact_id_123')
        
        contact_id = sync_service.sync_user_to_contact(user_data)
        
        assert contact_id == 'contact_id_123'
        sync_service.client.upsert_record.assert_called_once()
        call_args = sync_service.client.upsert_record.call_args
        assert call_args[1]['sobject_type'] == 'Contact'
        assert call_args[1]['external_id_field'] == 'User_External_Id__c'
        assert call_args[1]['external_id'] == 'user_123'
    
    def test_sync_user_with_full_name(self, sync_service):
        """Test syncing user with full name field"""
        user_data = {
            'user_id': 'user_123',
            'email': 'john@example.com',
            'name': 'John Doe Smith',
            'plan_type': 'free',
            'credits': 3
        }
        
        sync_service.client.upsert_record = Mock(return_value='contact_id_123')
        
        contact_id = sync_service.sync_user_to_contact(user_data)
        
        assert contact_id == 'contact_id_123'
        call_args = sync_service.client.upsert_record.call_args[1]['data']
        assert call_args['FirstName'] == 'John'
        assert call_args['LastName'] == 'Doe Smith'
    
    def test_sync_project_to_salesforce_success(self, sync_service):
        """Test syncing project to Salesforce"""
        project_data = {
            'project_id': 'proj_123',
            'user_id': 'user_123',
            'title': 'My First Film',
            'script': 'A story about...',
            'status': 'draft'
        }
        
        # Mock contact lookup
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'contact_id_123'})
        sync_service.client.upsert_record = Mock(return_value='project_id_sf')
        
        project_id = sync_service.sync_project_to_salesforce(project_data)
        
        assert project_id == 'project_id_sf'
        sync_service.client.upsert_record.assert_called_once()
    
    def test_sync_project_without_contact(self, sync_service):
        """Test syncing project when contact not found"""
        project_data = {
            'project_id': 'proj_123',
            'user_id': 'user_123',
            'title': 'Test',
            'script': 'Test',
            'status': 'draft'
        }
        
        sync_service.client.find_by_external_id = Mock(return_value=None)
        
        project_id = sync_service.sync_project_to_salesforce(project_data)
        
        assert project_id is None
    
    def test_update_project_status_completed(self, sync_service):
        """Test updating project status to completed"""
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'sf_proj_123'})
        sync_service.client.update_record = Mock(return_value=True)
        
        result = sync_service.update_project_status(
            'proj_123',
            'completed',
            video_url='https://example.com/video.mp4',
            completed_at=datetime(2025, 12, 31)
        )
        
        assert result is True
        call_args = sync_service.client.update_record.call_args[0]
        assert call_args[0] == 'AI_Project__c'
        assert call_args[1] == 'sf_proj_123'
        update_data = call_args[2]
        assert update_data['Status__c'] == 'completed'
        assert 'Video_URL__c' in update_data
    
    def test_update_project_status_failed(self, sync_service):
        """Test updating project status to failed"""
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'sf_proj_123'})
        sync_service.client.update_record = Mock(return_value=True)
        
        result = sync_service.update_project_status(
            'proj_123',
            'failed',
            error_message='GPU out of memory'
        )
        
        assert result is True
        call_args = sync_service.client.update_record.call_args[0]
        update_data = call_args[2]
        assert update_data['Status__c'] == 'failed'
        assert 'Error_Message__c' in update_data
    
    def test_sync_credit_record(self, sync_service):
        """Test syncing credit record"""
        credit_data = {
            'user_id': 'user_123',
            'plan_type': 'pro',
            'credits_allocated': 30,
            'credits_used': 0,
            'reset_date': datetime(2025, 1, 31),
            'status': 'active'
        }
        
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'contact_id_123'})
        sync_service.client.create_record = Mock(return_value='credit_id_123')
        
        credit_id = sync_service.sync_credit_record(credit_data)
        
        assert credit_id == 'credit_id_123'
        sync_service.client.create_record.assert_called_once()
    
    def test_update_credit_usage(self, sync_service):
        """Test updating credit usage"""
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'contact_id_123'})
        sync_service.client.query = Mock(return_value={
            'totalSize': 1,
            'records': [{
                'Id': 'credit_id_123',
                'Credits_Allocated__c': 30,
                'Credits_Used__c': 5
            }]
        })
        sync_service.client.update_record = Mock(return_value=True)
        
        result = sync_service.update_credit_usage('user_123', 15)
        
        assert result is True
        # Should update both credit record and contact
        assert sync_service.client.update_record.call_count == 2
    
    def test_sync_youtube_upload(self, sync_service):
        """Test syncing YouTube upload"""
        youtube_data = {
            'project_id': 'proj_123',
            'channel_id': 'UCxxxxxx',
            'video_id': 'dQw4w9WgXcQ',
            'upload_status': 'completed'
        }
        
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'proj_sf_123'})
        sync_service.client.create_record = Mock(return_value='youtube_id_123')
        
        youtube_id = sync_service.sync_youtube_upload(youtube_data)
        
        assert youtube_id == 'youtube_id_123'
        sync_service.client.create_record.assert_called_once()
        call_args = sync_service.client.create_record.call_args[0]
        assert call_args[0] == 'YouTube_Integration__c'
    
    def test_create_task_for_job_status(self, sync_service):
        """Test creating task for job status notification"""
        task_data = {
            'user_id': 'user_123',
            'subject': 'Video Generation Complete',
            'status': 'Completed',
            'description': 'Your video is ready'
        }
        
        sync_service.client.find_by_external_id = Mock(return_value={'Id': 'contact_id_123'})
        sync_service.client.create_record = Mock(return_value='task_id_123')
        
        task_id = sync_service.create_task_for_job_status(task_data)
        
        assert task_id == 'task_id_123'
        sync_service.client.create_record.assert_called_once()
        call_args = sync_service.client.create_record.call_args[0]
        assert call_args[0] == 'Task'


class TestModels:
    """Test Pydantic models"""
    
    def test_contact_model_valid(self):
        """Test ContactModel with valid data"""
        contact = ContactModel(
            LastName='Doe',
            Email='john@example.com',
            Plan_Type__c='pro',
            Credits__c=30,
            User_External_Id__c='user_123'
        )
        
        assert contact.LastName == 'Doe'
        assert contact.Email == 'john@example.com'
        assert contact.Plan_Type__c == 'pro'
    
    def test_ai_project_model_valid(self):
        """Test AIProjectModel with valid data"""
        project = AIProjectModel(
            Name='Test Project',
            Script__c='Test script',
            Status__c='draft',
            Project_External_Id__c='proj_123'
        )
        
        assert project.Name == 'Test Project'
        assert project.Status__c == 'draft'
        assert project.Project_External_Id__c == 'proj_123'
    
    def test_ai_credit_model_calculation(self):
        """Test AICreditModel with credits calculation"""
        credit = AICreditModel(
            Name='Test Credit',
            Contact__c='contact_123',
            Plan_Type__c='pro',
            Credits_Allocated__c=30,
            Credits_Used__c=10,
            Credits_Remaining__c=20,
            Reset_Date__c=datetime(2025, 1, 31),
            Status__c='active'
        )
        
        assert credit.Credits_Allocated__c == 30
        assert credit.Credits_Used__c == 10
        assert credit.Credits_Remaining__c == 20
    
    def test_youtube_integration_model(self):
        """Test YouTubeIntegrationModel"""
        youtube = YouTubeIntegrationModel(
            Name='Upload-1',
            AI_Project__c='proj_sf_123',
            Channel_Id__c='UCxxxxxx',
            Upload_Status__c='completed'
        )
        
        assert youtube.Channel_Id__c == 'UCxxxxxx'
        assert youtube.Upload_Status__c == 'completed'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
