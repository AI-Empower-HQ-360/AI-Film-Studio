"""
Simple notification sender for AI Film Studio.

This module provides basic functionality to send update notifications
about the film production process.
"""

import json
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional


class NotificationType(str, Enum):
    """Valid notification types."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class NotificationSender:
    """Sends update notifications for AI Film Studio."""
    
    def __init__(self):
        """Initialize the notification sender."""
        self.notifications = []
    
    def send_notification(
        self,
        message: str,
        notification_type: str = NotificationType.INFO,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a notification.
        
        Args:
            message: The notification message to send
            notification_type: Type of notification (info, warning, error, success)
            metadata: Optional additional metadata
        
        Returns:
            Dict containing the notification details
        """
        # Validate notification type
        if isinstance(notification_type, str):
            valid_types = [t.value for t in NotificationType]
            if notification_type not in valid_types:
                raise ValueError(
                    f"Invalid notification_type: {notification_type}. "
                    f"Must be one of: {', '.join(valid_types)}"
                )
        elif isinstance(notification_type, NotificationType):
            notification_type = notification_type.value
        notification = {
            "message": message,
            "type": notification_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        self.notifications.append(notification)
        
        # In a real implementation, this would send via email, webhook, etc.
        print(f"[{notification['type'].upper()}] {notification['message']}")
        
        return notification
    
    def get_notifications(self) -> list:
        """Get all sent notifications."""
        return self.notifications
    
    def send_update(
        self,
        stage: str,
        status: str,
        details: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a production update notification.
        
        Args:
            stage: Production stage (script, scenes, shots, video, export)
            status: Status of the stage (started, in_progress, completed, failed)
            details: Optional additional details
        
        Returns:
            Dict containing the notification details
        """
        message = f"Film Studio Update: {stage} - {status}"
        if details:
            message += f" - {details}"
        
        metadata = {
            "stage": stage,
            "status": status
        }
        
        notification_type = NotificationType.SUCCESS if status == "completed" else NotificationType.INFO
        if status == "failed":
            notification_type = NotificationType.ERROR
        
        return self.send_notification(message, notification_type, metadata)


def main():
    """Example usage of the notification sender."""
    sender = NotificationSender()
    
    # Send various types of notifications
    sender.send_update("script", "started", "Beginning script analysis")
    sender.send_update("script", "completed", "Script analysis finished")
    sender.send_update("scenes", "in_progress", "Processing 5 scenes")
    sender.send_update("shots", "started", "Generating shots from scenes")
    
    print("\n--- All Notifications ---")
    for notif in sender.get_notifications():
        print(json.dumps(notif, indent=2))


if __name__ == "__main__":
    main()
