"""Salesforce CRM Integration Configuration"""

# Salesforce Custom Objects Configuration
# This file documents the Salesforce CRM objects and fields for AI Film Studio

SALESFORCE_OBJECTS = {
    "Contact": {
        "description": "Standard Contact object enhanced with custom fields",
        "custom_fields": [
            {
                "api_name": "Subscription_Tier__c",
                "label": "Subscription Tier",
                "type": "Picklist",
                "values": ["Free", "Standard", "Pro", "Enterprise"],
                "description": "User's current subscription tier"
            },
            {
                "api_name": "Credits_Balance__c",
                "label": "Credits Balance",
                "type": "Number",
                "description": "Current credit balance"
            },
            {
                "api_name": "Credits_Reset_Date__c",
                "label": "Credits Reset Date",
                "type": "Date",
                "description": "Next monthly credit reset date"
            },
            {
                "api_name": "Last_Video_Generation__c",
                "label": "Last Video Generation",
                "type": "DateTime",
                "description": "Timestamp of last video generated"
            },
            {
                "api_name": "Total_Videos_Generated__c",
                "label": "Total Videos Generated",
                "type": "Number",
                "description": "Lifetime count of videos generated"
            }
        ]
    },
    
    "AI_Project__c": {
        "description": "Custom object for tracking AI video projects",
        "api_name": "AI_Project__c",
        "fields": [
            {
                "api_name": "Name",
                "label": "Project Name",
                "type": "Text",
                "length": 255,
                "required": True,
                "description": "Project title"
            },
            {
                "api_name": "User__c",
                "label": "User",
                "type": "Lookup",
                "relationship": "Contact",
                "required": True,
                "description": "Project owner"
            },
            {
                "api_name": "Script__c",
                "label": "Script",
                "type": "Long Text Area",
                "length": 32000,
                "description": "Video script content"
            },
            {
                "api_name": "Status__c",
                "label": "Status",
                "type": "Picklist",
                "values": ["Draft", "Processing", "Completed", "Failed"],
                "default": "Draft",
                "description": "Project status"
            },
            {
                "api_name": "Video_URL__c",
                "label": "Video URL",
                "type": "URL",
                "description": "S3 URL of final video"
            },
            {
                "api_name": "Thumbnail_URL__c",
                "label": "Thumbnail URL",
                "type": "URL",
                "description": "S3 URL of thumbnail"
            },
            {
                "api_name": "Subtitle_URLs__c",
                "label": "Subtitle URLs",
                "type": "Long Text Area",
                "description": "JSON of subtitle URLs by language"
            },
            {
                "api_name": "Duration_Minutes__c",
                "label": "Duration (Minutes)",
                "type": "Number",
                "decimal_places": 2,
                "description": "Video duration in minutes"
            },
            {
                "api_name": "Credits_Used__c",
                "label": "Credits Used",
                "type": "Number",
                "description": "Credits consumed for this project"
            },
            {
                "api_name": "Settings__c",
                "label": "Settings",
                "type": "Long Text Area",
                "description": "JSON of project settings (voice, music, etc.)"
            }
        ]
    },
    
    "AI_Credit__c": {
        "description": "Custom object for credit transactions",
        "api_name": "AI_Credit__c",
        "fields": [
            {
                "api_name": "User__c",
                "label": "User",
                "type": "Lookup",
                "relationship": "Contact",
                "required": True,
                "description": "User who performed transaction"
            },
            {
                "api_name": "Transaction_Type__c",
                "label": "Transaction Type",
                "type": "Picklist",
                "values": ["Purchase", "Deduction", "Grant", "Refund"],
                "required": True,
                "description": "Type of credit transaction"
            },
            {
                "api_name": "Amount__c",
                "label": "Amount",
                "type": "Number",
                "required": True,
                "description": "Credit amount (negative for deductions)"
            },
            {
                "api_name": "Balance_After__c",
                "label": "Balance After",
                "type": "Number",
                "required": True,
                "description": "Credit balance after transaction"
            },
            {
                "api_name": "Description__c",
                "label": "Description",
                "type": "Text",
                "length": 255,
                "description": "Transaction description"
            },
            {
                "api_name": "Project__c",
                "label": "Project",
                "type": "Lookup",
                "relationship": "AI_Project__c",
                "description": "Related project (if applicable)"
            },
            {
                "api_name": "Payment_ID__c",
                "label": "Payment ID",
                "type": "Text",
                "length": 255,
                "description": "Stripe/PayPal payment ID"
            }
        ]
    },
    
    "YouTube_Integration__c": {
        "description": "Custom object for YouTube upload tracking",
        "api_name": "YouTube_Integration__c",
        "fields": [
            {
                "api_name": "User__c",
                "label": "User",
                "type": "Lookup",
                "relationship": "Contact",
                "required": True,
                "description": "User who uploaded video"
            },
            {
                "api_name": "Project__c",
                "label": "Project",
                "type": "Lookup",
                "relationship": "AI_Project__c",
                "required": True,
                "description": "Related AI project"
            },
            {
                "api_name": "Video_ID__c",
                "label": "YouTube Video ID",
                "type": "Text",
                "length": 255,
                "description": "YouTube video identifier"
            },
            {
                "api_name": "Playlist_ID__c",
                "label": "YouTube Playlist ID",
                "type": "Text",
                "length": 255,
                "description": "YouTube playlist identifier"
            },
            {
                "api_name": "Upload_Status__c",
                "label": "Upload Status",
                "type": "Picklist",
                "values": ["Pending", "Uploading", "Completed", "Failed"],
                "default": "Pending",
                "description": "Upload status"
            },
            {
                "api_name": "YouTube_URL__c",
                "label": "YouTube URL",
                "type": "URL",
                "description": "Full YouTube video URL"
            },
            {
                "api_name": "Thumbnail_URL__c",
                "label": "Thumbnail URL",
                "type": "URL",
                "description": "YouTube thumbnail URL"
            },
            {
                "api_name": "Metadata__c",
                "label": "Metadata",
                "type": "Long Text Area",
                "description": "JSON of video metadata"
            }
        ]
    }
}

# Salesforce Automation Configuration
SALESFORCE_AUTOMATION = {
    "flows": [
        {
            "name": "Credit Deduction Flow",
            "trigger": "When AI_Project__c Status__c changes to 'Processing'",
            "actions": [
                "Get Credits_Used__c from AI_Project__c",
                "Get current Credits_Balance__c from Contact",
                "Check if Credits_Balance__c >= Credits_Used__c",
                "If insufficient: Stop processing and notify user",
                "If sufficient: Deduct credits from Contact.Credits_Balance__c",
                "Create AI_Credit__c record with type 'Deduction'"
            ]
        },
        {
            "name": "Monthly Credit Reset Flow",
            "trigger": "Scheduled daily at 00:00 UTC",
            "actions": [
                "Query Contacts where Credits_Reset_Date__c = TODAY",
                "For each Contact:",
                "  Reset Credits_Balance__c based on Subscription_Tier__c",
                "  Set Credits_Reset_Date__c to next month",
                "  Create AI_Credit__c record with type 'Grant'"
            ]
        },
        {
            "name": "Failed Job Refund Flow",
            "trigger": "When AI_Project__c Status__c changes to 'Failed'",
            "actions": [
                "Get Credits_Used__c from AI_Project__c",
                "If Credits_Used__c > 0:",
                "  Add credits back to Contact.Credits_Balance__c",
                "  Create AI_Credit__c record with type 'Refund'",
                "  Send email notification to user"
            ]
        }
    ],
    
    "process_builder": [
        {
            "name": "Update User Statistics",
            "trigger": "When AI_Project__c Status__c changes to 'Completed'",
            "actions": [
                "Update Contact.Total_Videos_Generated__c (increment by 1)",
                "Update Contact.Last_Video_Generation__c to NOW"
            ]
        }
    ],
    
    "apex_triggers": [
        {
            "name": "validateCreditBalance",
            "object": "AI_Project__c",
            "trigger_type": "Before Update",
            "logic": """
            When Status__c changes to 'Processing':
            1. Calculate credits required (Duration_Minutes__c * 3)
            2. Query Contact for current Credits_Balance__c
            3. If insufficient credits: Add error and prevent save
            4. If sufficient: Allow save (Flow will deduct credits)
            """
        },
        {
            "name": "syncWithExternalAPI",
            "object": "AI_Project__c",
            "trigger_type": "After Update",
            "logic": """
            When Video_URL__c or Status__c changes:
            1. Call external API to sync data
            2. Log sync result
            """
        }
    ]
}

# Salesforce Reports and Dashboards
SALESFORCE_ANALYTICS = {
    "dashboards": [
        {
            "name": "User Activity Dashboard",
            "components": [
                "Daily Active Users (last 30 days)",
                "New User Registrations (last 7 days)",
                "User Distribution by Subscription Tier",
                "Credit Balance Distribution"
            ]
        },
        {
            "name": "Revenue Dashboard",
            "components": [
                "Monthly Recurring Revenue (MRR)",
                "Revenue by Subscription Tier",
                "New Subscriptions vs Cancellations",
                "Average Revenue Per User (ARPU)"
            ]
        },
        {
            "name": "AI Usage Dashboard",
            "components": [
                "Videos Generated per Day",
                "Average Video Duration",
                "Credit Consumption Trend",
                "Most Popular Video Styles"
            ]
        },
        {
            "name": "System Health Dashboard",
            "components": [
                "Project Status Distribution",
                "Failed Jobs (last 24 hours)",
                "Average Processing Time",
                "YouTube Upload Success Rate"
            ]
        }
    ],
    
    "reports": [
        {
            "name": "Daily Active Users",
            "object": "Contact",
            "filters": [
                "Last_Video_Generation__c = LAST_N_DAYS:30"
            ],
            "group_by": "CreatedDate"
        },
        {
            "name": "Videos Generated by Tier",
            "object": "AI_Project__c",
            "join": "Contact (User__c)",
            "filters": [
                "Status__c = Completed"
            ],
            "group_by": "Contact.Subscription_Tier__c"
        },
        {
            "name": "Credit Transactions",
            "object": "AI_Credit__c",
            "filters": [
                "CreatedDate = THIS_MONTH"
            ],
            "group_by": "Transaction_Type__c",
            "summary": "SUM(Amount__c)"
        }
    ]
}

# API Integration Configuration
SALESFORCE_API_CONFIG = {
    "endpoint": "https://your-instance.salesforce.com",
    "api_version": "v58.0",
    "authentication": "OAuth 2.0",
    "required_permissions": [
        "API Enabled",
        "View All Data",
        "Modify All Data (for automation)"
    ],
    "rest_api_endpoints": {
        "create_project": "POST /services/data/v58.0/sobjects/AI_Project__c",
        "update_project": "PATCH /services/data/v58.0/sobjects/AI_Project__c/{id}",
        "create_credit_transaction": "POST /services/data/v58.0/sobjects/AI_Credit__c",
        "query_user": "GET /services/data/v58.0/query?q=SELECT+Id,Email,Credits_Balance__c+FROM+Contact+WHERE+Email='{email}'"
    }
}

if __name__ == "__main__":
    import json
    print("Salesforce Objects Configuration:")
    print(json.dumps(SALESFORCE_OBJECTS, indent=2))
