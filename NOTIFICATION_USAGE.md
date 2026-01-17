# Notification System Usage

The `send_notification.py` module provides a simple notification system for sending updates about the AI Film Studio production process.

## Features

- Send notifications with different types (info, warning, error, success)
- Track notification history
- Send production stage updates
- Timestamp all notifications with UTC timezone

## Usage

### Basic Example

```python
from send_notification import NotificationSender

# Create a sender instance
sender = NotificationSender()

# Send a simple notification
sender.send_notification(
    message="Processing started",
    notification_type="info"
)

# Send a production update
sender.send_update(
    stage="video",
    status="completed",
    details="Video exported successfully to MP4"
)

# Get all notifications
all_notifications = sender.get_notifications()
```

### Production Stages

The notification system supports the following production stages:
- `script` - Script parsing and generation
- `scenes` - Scene analysis and breakdown
- `shots` - Shot generation and composition  
- `video` - Video assembly and processing
- `export` - Final export to MP4

### Status Types

- `started` - Stage has begun
- `in_progress` - Stage is actively processing
- `completed` - Stage finished successfully
- `failed` - Stage encountered an error

### Notification Types

- `info` - General information
- `warning` - Warning message
- `error` - Error occurred
- `success` - Successful operation

## Running the Example

```bash
python send_notification.py
```

This will run a demonstration that shows various notification types and displays all sent notifications.

## Future Enhancements

In a production environment, this module could be extended to:
- Send emails via SMTP
- Post to webhooks or Slack channels
- Store notifications in a database
- Implement real-time WebSocket notifications
- Add user preferences for notification delivery
