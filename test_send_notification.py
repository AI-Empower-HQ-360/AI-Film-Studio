"""
Unit tests for the notification sender module.
"""

import unittest
from datetime import datetime, timezone
from send_notification import NotificationSender, NotificationType


class TestNotificationSender(unittest.TestCase):
    """Test cases for NotificationSender class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sender = NotificationSender()
    
    def test_send_notification_basic(self):
        """Test sending a basic notification."""
        result = self.sender.send_notification("Test message")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["message"], "Test message")
        self.assertEqual(result["type"], "info")
        self.assertIn("timestamp", result)
        self.assertIn("metadata", result)
    
    def test_send_notification_with_type(self):
        """Test sending notifications with different types."""
        types = ["info", "warning", "error", "success"]
        
        for notif_type in types:
            result = self.sender.send_notification(
                f"Test {notif_type}",
                notification_type=notif_type
            )
            self.assertEqual(result["type"], notif_type)
    
    def test_send_notification_with_metadata(self):
        """Test sending a notification with metadata."""
        metadata = {"key": "value", "count": 42}
        result = self.sender.send_notification(
            "Test with metadata",
            metadata=metadata
        )
        
        self.assertEqual(result["metadata"], metadata)
    
    def test_get_notifications(self):
        """Test retrieving all notifications."""
        self.sender.send_notification("Message 1")
        self.sender.send_notification("Message 2")
        self.sender.send_notification("Message 3")
        
        notifications = self.sender.get_notifications()
        self.assertEqual(len(notifications), 3)
        self.assertEqual(notifications[0]["message"], "Message 1")
        self.assertEqual(notifications[1]["message"], "Message 2")
        self.assertEqual(notifications[2]["message"], "Message 3")
    
    def test_send_update(self):
        """Test sending a production update."""
        result = self.sender.send_update(
            stage="script",
            status="completed",
            details="Analysis finished"
        )
        
        self.assertIn("Film Studio Update", result["message"])
        self.assertIn("script", result["message"])
        self.assertIn("completed", result["message"])
        self.assertIn("Analysis finished", result["message"])
        self.assertEqual(result["metadata"]["stage"], "script")
        self.assertEqual(result["metadata"]["status"], "completed")
    
    def test_send_update_notification_type(self):
        """Test that send_update uses correct notification types."""
        # Test completed status -> success
        result = self.sender.send_update("video", "completed")
        self.assertEqual(result["type"], "success")
        
        # Test failed status -> error
        result = self.sender.send_update("export", "failed")
        self.assertEqual(result["type"], "error")
        
        # Test other statuses -> info
        result = self.sender.send_update("scenes", "started")
        self.assertEqual(result["type"], "info")
        
        result = self.sender.send_update("shots", "in_progress")
        self.assertEqual(result["type"], "info")
    
    def test_timestamp_format(self):
        """Test that timestamps are in correct ISO format with timezone."""
        result = self.sender.send_notification("Test timestamp")
        timestamp_str = result["timestamp"]
        
        # Should be able to parse as ISO format
        timestamp = datetime.fromisoformat(timestamp_str)
        self.assertIsNotNone(timestamp)
        
        # Should include timezone info (UTC)
        self.assertIsNotNone(timestamp.tzinfo)
    
    def test_empty_notifications_initially(self):
        """Test that a new sender has no notifications."""
        new_sender = NotificationSender()
        self.assertEqual(len(new_sender.get_notifications()), 0)
    
    def test_notification_ordering(self):
        """Test that notifications are returned in order sent."""
        for i in range(5):
            self.sender.send_notification(f"Message {i}")
        
        notifications = self.sender.get_notifications()
        for i in range(5):
            self.assertEqual(notifications[i]["message"], f"Message {i}")
    
    def test_notification_type_enum(self):
        """Test that NotificationType enum can be used."""
        result = self.sender.send_notification(
            "Test with enum",
            notification_type=NotificationType.WARNING
        )
        self.assertEqual(result["type"], "warning")
    
    def test_invalid_notification_type(self):
        """Test that invalid notification type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.sender.send_notification(
                "Test invalid",
                notification_type="invalid_type"
            )
        self.assertIn("Invalid notification_type", str(context.exception))
        self.assertIn("invalid_type", str(context.exception))


if __name__ == "__main__":
    unittest.main()
