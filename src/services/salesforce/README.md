# Salesforce CRM Integration

This directory contains the complete implementation of Salesforce CRM integration for AI Film Studio.

## Overview

The Salesforce CRM integration enables seamless synchronization between AI Film Studio and Salesforce, allowing you to:

- Track users as Salesforce Contacts
- Monitor AI project lifecycle in custom objects
- Manage credit allocations and usage
- Record YouTube upload status
- Automate notifications and workflows

## Features

✅ **Real-time Data Sync**: Background tasks ensure data is synced without blocking user requests  
✅ **Custom Objects**: Purpose-built Salesforce objects for AI projects, credits, and YouTube integrations  
✅ **Automation Ready**: Includes Flow, Process Builder, and Apex trigger examples  
✅ **API Endpoints**: RESTful endpoints for integration and webhooks  
✅ **Comprehensive Testing**: Full test coverage with mocked Salesforce API  
✅ **Enterprise-Ready**: Handles errors gracefully and respects API limits

## Architecture

```
src/services/salesforce/
├── __init__.py           # Module exports
├── client.py             # Salesforce API client wrapper
├── models.py             # Pydantic models for Salesforce objects
└── sync_service.py       # Data synchronization service

src/api/
└── salesforce_routes.py  # API endpoints for sync and webhooks

docs/integrations/
├── salesforce-crm-integration.md         # Complete integration guide
└── salesforce-automation-examples.md     # Apex code and Flow examples

tests/
└── test_salesforce_integration.py        # Comprehensive test suite
```

## Quick Start

### 1. Install Dependencies

```bash
pip install simple-salesforce salesforce-bulk
```

### 2. Configure Environment

Add to your `.env` file:

```bash
SALESFORCE_USERNAME=your_username@salesforce.com
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_security_token
SALESFORCE_DOMAIN=login  # or 'test' for sandbox
SALESFORCE_SYNC_ENABLED=true
```

### 3. Create Custom Objects

Follow the instructions in `docs/integrations/salesforce-crm-integration.md` to:
- Create custom fields on Contact
- Create AI_Project__c custom object
- Create AI_Credit__c custom object
- Create YouTube_Integration__c custom object

### 4. Test the Integration

```bash
# Run tests
pytest tests/test_salesforce_integration.py -v

# Test API health
curl http://localhost:8000/api/v1/salesforce/health
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/salesforce/sync/user` | POST | Sync user to Salesforce Contact |
| `/api/v1/salesforce/sync/project` | POST | Sync project to AI_Project__c |
| `/api/v1/salesforce/update/project-status` | POST | Update project status |
| `/api/v1/salesforce/update/credits` | POST | Update credit usage |
| `/api/v1/salesforce/sync/youtube-upload` | POST | Sync YouTube upload |
| `/api/v1/salesforce/webhook` | POST | Receive Salesforce webhooks |
| `/api/v1/salesforce/health` | GET | Check connection status |

## Usage Examples

### Sync User

```python
from src.services.salesforce import SalesforceSyncService

service = SalesforceSyncService()
user_data = {
    'user_id': 'user_123',
    'email': 'john@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'plan_type': 'pro',
    'credits': 30
}
contact_id = service.sync_user_to_contact(user_data)
```

### Update Project Status

```python
success = service.update_project_status(
    project_id='proj_456',
    status='completed',
    video_url='https://s3.amazonaws.com/video.mp4',
    completed_at=datetime.now()
)
```

### REST API

```bash
# Sync user via API
curl -X POST http://localhost:8000/api/v1/salesforce/sync/user \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "plan_type": "pro",
    "credits": 30
  }'
```

## Salesforce Objects

### Contact (Standard Object)

Maps to AI Film Studio users. Custom fields:
- `Plan_Type__c`: Subscription tier (free, pro, enterprise)
- `Credits__c`: Current credit balance
- `User_External_Id__c`: Links to internal user ID
- `Last_Login__c`: Last login timestamp

### AI_Project__c (Custom Object)

Tracks film projects through their lifecycle:
- `Script__c`: Project script text
- `Status__c`: Current status (draft, queued, processing, completed, failed)
- `Video_URL__c`: Final video URL
- `Contact__c`: Lookup to project owner
- `Project_External_Id__c`: Links to internal project ID

### AI_Credit__c (Custom Object)

Manages subscription plans and credit allocations:
- `Plan_Type__c`: Subscription plan
- `Credits_Allocated__c`: Total credits for period
- `Credits_Used__c`: Credits consumed
- `Credits_Remaining__c`: Formula field (Allocated - Used)
- `Reset_Date__c`: Monthly reset date

### YouTube_Integration__c (Custom Object)

Records YouTube video uploads:
- `Channel_Id__c`: YouTube channel ID
- `Video_Id__c`: YouTube video ID
- `Upload_Status__c`: Upload status
- `AI_Project__c`: Link to source project

## Automation

### Email Notifications

When a project status changes to "completed", automatically send an email to the user with the video download link.

**Implementation**: Record-Triggered Flow on AI_Project__c

### Credit Deduction

Automatically deduct credits when a project starts generation.

**Implementation**: Apex Trigger on AI_Project__c

### Failed Job Support

Create a support case when an AI job fails multiple times.

**Implementation**: Process Builder or Flow

See `docs/integrations/salesforce-automation-examples.md` for complete code examples.

## Testing

The test suite includes:

- **Client Tests**: Salesforce API wrapper functionality
- **Sync Service Tests**: Data synchronization logic
- **Model Tests**: Pydantic model validation
- **Integration Tests**: End-to-end sync workflows

Run all tests:
```bash
pytest tests/test_salesforce_integration.py -v --cov=src/services/salesforce
```

## Security Best Practices

1. **Never commit credentials**: Use environment variables
2. **Use IP restrictions**: Limit API access by IP in Salesforce
3. **Rotate tokens regularly**: Security tokens should be refreshed periodically
4. **Validate webhooks**: Implement signature validation for incoming webhooks
5. **Respect API limits**: Monitor daily API usage (15,000/day for Developer Edition)

## Troubleshooting

### Connection Issues

**Problem**: `SalesforceAuthenticationFailed`

**Solution**: 
- Verify credentials in `.env`
- Check security token
- Ensure API access is enabled for your user

### Record Not Found

**Problem**: External ID not found during upsert

**Solution**:
- Ensure external ID fields are marked as External ID and Unique
- Verify field-level security permissions

### API Limits

**Problem**: Daily API limit exceeded

**Solution**:
- Use bulk operations for large datasets
- Implement batch processing
- Upgrade Salesforce edition for higher limits

## Documentation

- **[Integration Guide](../../docs/integrations/salesforce-crm-integration.md)**: Complete setup and configuration
- **[Automation Examples](../../docs/integrations/salesforce-automation-examples.md)**: Apex code and Flow configurations
- **[API Documentation](http://localhost:8000/docs)**: Interactive API docs (when server is running)

## Support

For issues or questions:
- **GitHub Issues**: [AI-Film-Studio/issues](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
- **Salesforce Help**: [help.salesforce.com](https://help.salesforce.com)

## License

This integration is part of AI Film Studio and is licensed under the MIT License.

---

**Version**: 1.0  
**Last Updated**: 2025-12-31
