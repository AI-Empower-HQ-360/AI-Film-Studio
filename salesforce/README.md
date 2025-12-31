# Salesforce Integration - AI Film Studio

## Overview

This directory contains Salesforce metadata and integration components for AI Film Studio, including custom objects, flows, Apex classes, and reports.

## Structure

```
salesforce/
├── objects/              # Custom Salesforce objects
├── flows/                # Automation flows
├── apex/                 # Apex classes and triggers
└── reports-dashboards/   # Reports and dashboards
```

## Custom Objects

### AI_Project__c
Stores project metadata and status.

**Fields**:
- Name (Text)
- Status__c (Picklist: Draft, Processing, Completed, Failed)
- User__c (Lookup to User)
- Description__c (Long Text Area)
- Created_Date__c (Date/Time)
- Video_URL__c (URL)

### AI_Credit__c
Tracks user credit balance and transactions.

**Fields**:
- User__c (Lookup to User)
- Balance__c (Number)
- Transaction_Type__c (Picklist: Purchase, Usage, Refund)
- Amount__c (Number)
- Transaction_Date__c (Date/Time)

### AI_Job__c
Records AI job execution details.

**Fields**:
- Project__c (Lookup to AI_Project__c)
- Status__c (Picklist: Pending, Processing, Completed, Failed)
- Job_Type__c (Picklist: Script Analysis, Image Gen, Voice Synthesis, etc.)
- Result_URL__c (URL)
- Started_At__c (Date/Time)
- Completed_At__c (Date/Time)

## Automation Flows

### Credit Allocation Flow
Automatically allocates credits when subscription is created or renewed.

### Project Approval Flow
Approval process for enterprise users' projects.

### Job Notification Flow
Sends notifications when jobs complete or fail.

## Apex Classes

### AIProjectController
Handles project CRUD operations via REST API.

```apex
@RestResource(urlMapping='/api/projects/*')
global class AIProjectController {
    @HttpGet
    global static AI_Project__c getProject() {
        // Implementation
    }
    
    @HttpPost
    global static AI_Project__c createProject() {
        // Implementation
    }
}
```

### CreditManager
Manages credit transactions.

```apex
public class CreditManager {
    public static void allocateCredits(Id userId, Decimal amount) {
        // Implementation
    }
    
    public static Decimal getBalance(Id userId) {
        // Implementation
    }
}
```

### JobStatusUpdater
Updates job status from external system.

```apex
public class JobStatusUpdater {
    @future(callout=true)
    public static void updateStatus(Id jobId, String status) {
        // Implementation
    }
}
```

## Reports & Dashboards

### Reports

1. **User Activity Report**
   - Active users per month
   - Project creation trends
   - Video generation volume

2. **Credit Usage Report**
   - Credits consumed per user
   - Average credits per project
   - Revenue projections

3. **Project Status Report**
   - Projects by status
   - Completion rates
   - Failure analysis

### Dashboards

1. **Executive Dashboard**
   - User growth metrics
   - Revenue analytics
   - System health indicators

2. **Operations Dashboard**
   - Job queue depth
   - Processing times
   - Error rates
   - Resource utilization

## Integration

### REST API Integration

AI Film Studio backend integrates with Salesforce via REST API:

```python
import requests

def create_salesforce_project(project_data):
    url = f"{SF_INSTANCE_URL}/services/data/v58.0/sobjects/AI_Project__c"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=project_data, headers=headers)
    return response.json()
```

### OAuth 2.0 Authentication

```python
def get_salesforce_token():
    url = f"{SF_INSTANCE_URL}/services/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": SF_CLIENT_ID,
        "client_secret": SF_CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    return response.json()["access_token"]
```

## Deployment

### Using Salesforce CLI

```bash
# Authenticate
sfdx auth:web:login -a myorg

# Deploy metadata
sfdx force:source:deploy -p salesforce/ -u myorg

# Run tests
sfdx force:apex:test:run -u myorg
```

### Using VS Code

1. Install Salesforce Extension Pack
2. Authorize org
3. Right-click folder → Deploy Source to Org

## Testing

### Apex Unit Tests

```apex
@isTest
private class AIProjectControllerTest {
    @isTest
    static void testCreateProject() {
        AI_Project__c project = new AI_Project__c(
            Name = 'Test Project',
            Status__c = 'Draft'
        );
        insert project;
        
        System.assertNotEquals(null, project.Id);
    }
}
```

## License

MIT License - see [LICENSE](../LICENSE)
