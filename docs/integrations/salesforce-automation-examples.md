# Salesforce Automation Examples

**Version:** 1.0  
**Last Updated:** 2025-12-31

This document provides ready-to-use Salesforce automation code including Apex triggers, classes, and Flow configurations.

---

## Table of Contents

1. [Apex Triggers](#apex-triggers)
2. [Apex Classes](#apex-classes)
3. [Flow Configurations](#flow-configurations)
4. [Email Templates](#email-templates)
5. [Reports & Dashboards](#reports--dashboards)

---

## Apex Triggers

### 1. Credit Deduction Trigger

Automatically deduct credits when a project starts generation.

```apex
/**
 * Trigger: AI_Project_CreditDeduction
 * Object: AI_Project__c
 * Purpose: Deduct credits when project status changes to 'queued'
 */
trigger AI_Project_CreditDeduction on AI_Project__c (after update) {
    List<AI_Credit__c> creditsToUpdate = new List<AI_Credit__c>();
    
    for (AI_Project__c project : Trigger.new) {
        AI_Project__c oldProject = Trigger.oldMap.get(project.Id);
        
        // Check if status changed from draft to queued
        if (project.Status__c == 'queued' && oldProject.Status__c == 'draft') {
            // Find active credit record
            List<AI_Credit__c> credits = [
                SELECT Id, Credits_Used__c, Credits_Allocated__c, Credits_Remaining__c
                FROM AI_Credit__c
                WHERE Contact__c = :project.Contact__c
                AND Status__c = 'active'
                ORDER BY CreatedDate DESC
                LIMIT 1
            ];
            
            if (!credits.isEmpty()) {
                AI_Credit__c credit = credits[0];
                
                // Check if sufficient credits
                if (credit.Credits_Remaining__c >= 1) {
                    credit.Credits_Used__c = (credit.Credits_Used__c != null ? credit.Credits_Used__c : 0) + 1;
                    creditsToUpdate.add(credit);
                } else {
                    // Insufficient credits - mark project as failed
                    project.Status__c = 'failed';
                    project.Error_Message__c = 'Insufficient credits';
                }
            }
        }
    }
    
    if (!creditsToUpdate.isEmpty()) {
        update creditsToUpdate;
        
        // Update Contact credits as well
        List<Contact> contactsToUpdate = new List<Contact>();
        for (AI_Credit__c credit : creditsToUpdate) {
            Contact con = new Contact(
                Id = credit.Contact__c,
                Credits__c = credit.Credits_Remaining__c
            );
            contactsToUpdate.add(con);
        }
        update contactsToUpdate;
    }
}
```

**Test Class:**

```apex
@isTest
private class AI_Project_CreditDeduction_Test {
    
    @testSetup
    static void setup() {
        // Create test contact
        Contact testContact = new Contact(
            FirstName = 'Test',
            LastName = 'User',
            Email = 'test@example.com',
            User_External_Id__c = 'test_user_123',
            Plan_Type__c = 'pro',
            Credits__c = 30
        );
        insert testContact;
        
        // Create credit record
        AI_Credit__c credit = new AI_Credit__c(
            Name = 'PRO - test_user',
            Contact__c = testContact.Id,
            Plan_Type__c = 'pro',
            Credits_Allocated__c = 30,
            Credits_Used__c = 0,
            Reset_Date__c = Date.today().addMonths(1),
            Status__c = 'active'
        );
        insert credit;
        
        // Create project
        AI_Project__c project = new AI_Project__c(
            Name = 'Test Project',
            Script__c = 'Test script',
            Status__c = 'draft',
            Contact__c = testContact.Id,
            Project_External_Id__c = 'test_proj_456'
        );
        insert project;
    }
    
    @isTest
    static void testCreditDeduction() {
        AI_Project__c project = [SELECT Id, Status__c FROM AI_Project__c LIMIT 1];
        
        Test.startTest();
        project.Status__c = 'queued';
        update project;
        Test.stopTest();
        
        // Verify credit was deducted
        AI_Credit__c credit = [
            SELECT Credits_Used__c, Credits_Remaining__c 
            FROM AI_Credit__c 
            LIMIT 1
        ];
        System.assertEquals(1, credit.Credits_Used__c, 'Credit should be deducted');
        System.assertEquals(29, credit.Credits_Remaining__c, 'Remaining credits should be 29');
        
        // Verify contact credits updated
        Contact con = [SELECT Credits__c FROM Contact LIMIT 1];
        System.assertEquals(29, con.Credits__c, 'Contact credits should be updated');
    }
    
    @isTest
    static void testInsufficientCredits() {
        // Update credit to 0
        AI_Credit__c credit = [SELECT Id FROM AI_Credit__c LIMIT 1];
        credit.Credits_Used__c = 30;
        update credit;
        
        AI_Project__c project = [SELECT Id, Status__c FROM AI_Project__c LIMIT 1];
        
        Test.startTest();
        project.Status__c = 'queued';
        update project;
        Test.stopTest();
        
        // Verify project marked as failed
        project = [SELECT Status__c, Error_Message__c FROM AI_Project__c WHERE Id = :project.Id];
        System.assertEquals('failed', project.Status__c, 'Project should be marked as failed');
        System.assertEquals('Insufficient credits', project.Error_Message__c, 'Error message should be set');
    }
}
```

---

### 2. Project Status Update Notification

Send email when project status changes.

```apex
/**
 * Trigger: AI_Project_StatusNotification
 * Object: AI_Project__c
 * Purpose: Create task/notification when project status changes
 */
trigger AI_Project_StatusNotification on AI_Project__c (after update) {
    List<Task> tasksToCreate = new List<Task>();
    
    for (AI_Project__c project : Trigger.new) {
        AI_Project__c oldProject = Trigger.oldMap.get(project.Id);
        
        // Check if status changed
        if (project.Status__c != oldProject.Status__c) {
            String subject = '';
            String description = '';
            String priority = 'Normal';
            
            if (project.Status__c == 'completed') {
                subject = 'AI Film Generation Complete: ' + project.Name;
                description = 'Your AI film has been generated successfully. Video URL: ' + project.Video_URL__c;
                priority = 'High';
            } else if (project.Status__c == 'failed') {
                subject = 'AI Film Generation Failed: ' + project.Name;
                description = 'Film generation failed. Error: ' + project.Error_Message__c;
                priority = 'High';
            } else if (project.Status__c == 'processing') {
                subject = 'AI Film Generation In Progress: ' + project.Name;
                description = 'Your film is being generated. This may take a few minutes.';
            }
            
            if (subject != '') {
                Task newTask = new Task(
                    Subject = subject,
                    Description = description,
                    Priority = priority,
                    Status = 'Completed',
                    WhoId = project.Contact__c,
                    ActivityDate = Date.today()
                );
                tasksToCreate.add(newTask);
            }
        }
    }
    
    if (!tasksToCreate.isEmpty()) {
        insert tasksToCreate;
    }
}
```

---

## Apex Classes

### 1. YouTube Upload Status Checker

Scheduled job to check YouTube upload status.

```apex
/**
 * Class: YouTubeUploadStatusChecker
 * Purpose: Scheduled job to check and update YouTube upload status
 * Schedule: Run every hour
 */
global class YouTubeUploadStatusChecker implements Schedulable {
    
    global void execute(SchedulableContext sc) {
        checkPendingUploads();
    }
    
    @future(callout=true)
    public static void checkPendingUploads() {
        List<YouTube_Integration__c> uploadsToUpdate = new List<YouTube_Integration__c>();
        
        // Query pending/uploading records from last 7 days
        List<YouTube_Integration__c> pendingUploads = [
            SELECT Id, Video_Id__c, Upload_Status__c, Channel_Id__c
            FROM YouTube_Integration__c
            WHERE Upload_Status__c IN ('pending', 'uploading')
            AND CreatedDate = LAST_N_DAYS:7
            LIMIT 100
        ];
        
        for (YouTube_Integration__c upload : pendingUploads) {
            try {
                // Make callout to YouTube API (placeholder)
                String status = checkYouTubeStatus(upload.Video_Id__c);
                
                if (status == 'published') {
                    upload.Upload_Status__c = 'completed';
                    upload.Upload_Date__c = DateTime.now();
                } else if (status == 'failed') {
                    upload.Upload_Status__c = 'failed';
                    upload.Error_Message__c = 'YouTube upload failed';
                }
                
                uploadsToUpdate.add(upload);
            } catch (Exception e) {
                System.debug('Error checking upload status: ' + e.getMessage());
            }
        }
        
        if (!uploadsToUpdate.isEmpty()) {
            update uploadsToUpdate;
        }
    }
    
    // Placeholder for YouTube API callout
    private static String checkYouTubeStatus(String videoId) {
        // In production, this would make an actual API call
        // HttpRequest req = new HttpRequest();
        // req.setEndpoint('https://www.googleapis.com/youtube/v3/videos?id=' + videoId);
        // req.setMethod('GET');
        // Http http = new Http();
        // HttpResponse res = http.send(req);
        // Parse response and return status
        
        return 'published'; // Placeholder
    }
}

// Schedule the job
// System.schedule('YouTube Upload Check', '0 0 * * * ?', new YouTubeUploadStatusChecker());
```

---

### 2. Salesforce Data Sync Utility

Utility class for common sync operations.

```apex
/**
 * Class: SalesforceDataSyncUtil
 * Purpose: Utility methods for syncing data with external systems
 */
public class SalesforceDataSyncUtil {
    
    /**
     * Update project status and related records
     */
    public static void updateProjectStatus(String projectExternalId, String newStatus, String videoUrl, String errorMessage) {
        List<AI_Project__c> projects = [
            SELECT Id, Status__c, Contact__c
            FROM AI_Project__c
            WHERE Project_External_Id__c = :projectExternalId
            LIMIT 1
        ];
        
        if (!projects.isEmpty()) {
            AI_Project__c project = projects[0];
            project.Status__c = newStatus;
            
            if (newStatus == 'completed') {
                project.Completed_Date__c = DateTime.now();
                project.Video_URL__c = videoUrl;
            } else if (newStatus == 'failed') {
                project.Error_Message__c = errorMessage;
            }
            
            update project;
        }
    }
    
    /**
     * Bulk upsert contacts from external system
     */
    public static void bulkUpsertContacts(List<Contact> contacts) {
        Database.UpsertResult[] results = Database.upsert(contacts, Contact.User_External_Id__c, false);
        
        for (Integer i = 0; i < results.size(); i++) {
            if (!results[i].isSuccess()) {
                System.debug('Error upserting contact: ' + results[i].getErrors());
            }
        }
    }
    
    /**
     * Get active credit record for contact
     */
    public static AI_Credit__c getActiveCredit(Id contactId) {
        List<AI_Credit__c> credits = [
            SELECT Id, Credits_Allocated__c, Credits_Used__c, Credits_Remaining__c
            FROM AI_Credit__c
            WHERE Contact__c = :contactId
            AND Status__c = 'active'
            ORDER BY CreatedDate DESC
            LIMIT 1
        ];
        
        return credits.isEmpty() ? null : credits[0];
    }
}
```

---

## Flow Configurations

### Flow 1: Email Alert on Project Completion

**Flow Type**: Record-Triggered Flow  
**Object**: AI_Project__c  
**Trigger**: Record is updated

**Configuration:**

```yaml
Trigger:
  Object: AI_Project__c
  Trigger: A record is updated
  Entry Conditions:
    - Status__c EQUALS completed
    - ISCHANGED(Status__c) EQUALS true
  
Optimize Flow For: Actions and Related Records

Actions:
  1. Send Email:
      Recipients: {!$Record.Contact__c.Email}
      Subject: "Your AI Film is Ready!"
      Body (Rich Text):
        <p>Hi {!$Record.Contact__c.FirstName},</p>
        <p>Great news! Your AI film "<b>{!$Record.Name}</b>" has been generated successfully.</p>
        <p><a href="{!$Record.Video_URL__c}">Click here to download your video</a></p>
        <p>Duration: {!$Record.Duration__c} seconds</p>
        <p>Thank you for using AI Film Studio!</p>
```

**Setup Steps:**

1. Navigate to **Setup > Flows > New Flow**
2. Choose **Record-Triggered Flow**
3. Select Object: AI_Project__c
4. Trigger: A record is updated
5. Add Condition: Status__c = completed AND ISCHANGED(Status__c)
6. Add Action: Send Email
7. Activate Flow

---

### Flow 2: Create Support Case on Failed Jobs

**Flow Type**: Record-Triggered Flow  
**Object**: AI_Project__c  
**Trigger**: Record is updated

**Configuration:**

```yaml
Trigger:
  Object: AI_Project__c
  Trigger: A record is updated
  Entry Conditions:
    - Status__c EQUALS failed
    - ISCHANGED(Status__c) EQUALS true

Actions:
  1. Decision: Check Retry Count
      Outcome 1: Multiple Failures
        Condition: Failure_Count__c >= 3
      
  2. Create Case (if Multiple Failures):
      Fields:
        Subject: "AI Job Failed Multiple Times - {!$Record.Name}"
        Description: "Project: {!$Record.Name}\nError: {!$Record.Error_Message__c}\nExternal ID: {!$Record.Project_External_Id__c}"
        Priority: High
        Status: New
        ContactId: {!$Record.Contact__c}
        Origin: Web
        Type: Technical Issue
```

---

### Flow 3: Monthly Credit Reset

**Flow Type**: Scheduled Flow  
**Schedule**: First day of every month at 00:00

**Configuration:**

```yaml
Schedule:
  Frequency: Monthly
  Start Date: 2025-01-01
  Start Time: 00:00
  
Object: AI_Credit__c

Criteria:
  - Status__c EQUALS active
  - Reset_Date__c <= TODAY

Actions:
  1. Update Records:
      Fields to Update:
        - Credits_Used__c = 0
        - Reset_Date__c = {!$Flow.CurrentDate} + 30 days
```

---

## Email Templates

### Template 1: Video Generation Complete

**Template Name**: Video_Generation_Complete  
**Type**: Lightning Email Template  
**Folder**: AI Film Studio

**HTML Body:**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #00A1E0; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .button { background-color: #00A1E0; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 10px 0; }
        .footer { background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎬 Your AI Film is Ready!</h1>
    </div>
    <div class="content">
        <p>Hi {!Contact.FirstName},</p>
        
        <p>Great news! Your AI film "<strong>{!AI_Project__c.Name}</strong>" has been generated successfully.</p>
        
        <p>
            <a href="{!AI_Project__c.Video_URL__c}" class="button">Download Your Video</a>
        </p>
        
        <p><strong>Project Details:</strong></p>
        <ul>
            <li>Duration: {!AI_Project__c.Duration__c} seconds</li>
            <li>Status: {!AI_Project__c.Status__c}</li>
            <li>Completed: {!AI_Project__c.Completed_Date__c}</li>
        </ul>
        
        <p>Thank you for using AI Film Studio!</p>
        
        <p>Best regards,<br/>The AI Film Studio Team</p>
    </div>
    <div class="footer">
        <p>© 2025 AI Film Studio. All rights reserved.</p>
    </div>
</body>
</html>
```

---

### Template 2: Credit Low Warning

**Template Name**: Credit_Low_Warning  
**Type**: Lightning Email Template

**HTML Body:**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #FF9900; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .button { background-color: #00A1E0; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚠️ Low Credits Warning</h1>
    </div>
    <div class="content">
        <p>Hi {!Contact.FirstName},</p>
        
        <p>You're running low on credits! You currently have <strong>{!Contact.Credits__c}</strong> credits remaining.</p>
        
        <p>Don't miss out on creating more amazing AI films. Top up your credits or upgrade your plan.</p>
        
        <p>
            <a href="https://aifilmstudio.com/pricing" class="button">Upgrade Now</a>
        </p>
        
        <p><strong>Current Plan:</strong> {!Contact.Plan_Type__c}</p>
        <p><strong>Credits Remaining:</strong> {!Contact.Credits__c}</p>
        
        <p>Best regards,<br/>The AI Film Studio Team</p>
    </div>
</body>
</html>
```

---

## Reports & Dashboards

### Report 1: Projects by Status

**Report Type**: AI Projects  
**Report Format**: Summary

**Columns:**
- Project Name
- Contact Name
- Status
- Created Date
- Completed Date
- Video URL

**Grouping:** Group by Status

**Filters:**
- Created Date = THIS_MONTH

---

### Report 2: Credit Usage by Plan Type

**Report Type**: AI Credits with Contacts  
**Report Format**: Summary

**Columns:**
- Contact Name
- Plan Type
- Credits Allocated
- Credits Used
- Credits Remaining
- Status

**Grouping:** Group by Plan Type

**Summary Fields:**
- SUM(Credits_Allocated__c)
- SUM(Credits_Used__c)
- AVG(Credits_Remaining__c)

---

### Dashboard: AI Film Studio Analytics

**Components:**

1. **Total Projects by Status** (Donut Chart)
   - Source: Projects by Status report
   - Group by Status
   
2. **Projects Created This Month** (Metric)
   - Source: Projects report
   - Filter: Created Date = THIS_MONTH
   
3. **Credit Usage by Plan** (Bar Chart)
   - Source: Credit Usage report
   - X-axis: Plan Type
   - Y-axis: Credits Used
   
4. **Failed Projects** (Table)
   - Source: Projects report
   - Filter: Status = failed
   - Sort: Created Date DESC

---

## Deployment Checklist

- [ ] Deploy all Apex classes and triggers
- [ ] Deploy test classes (minimum 75% code coverage)
- [ ] Create and activate all Flows
- [ ] Create email templates
- [ ] Create reports and dashboards
- [ ] Schedule batch jobs
- [ ] Test all automations in Sandbox
- [ ] Document any custom configurations

---

**Last Updated**: 2025-12-31  
**Version**: 1.0
