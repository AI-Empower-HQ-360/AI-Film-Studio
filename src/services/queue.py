"""
SQS Queue Service for AI Film Studio.
Handles message queue operations for async job processing.
"""

import os
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime


class QueueService:
    """AWS SQS Queue Service for managing async job queues."""
    
    def __init__(self, queue_url: Optional[str] = None):
        """Initialize the queue service."""
        self.queue_url = queue_url or os.getenv("SQS_QUEUE_URL", "")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self._client = None
        self._messages: Dict[str, Dict[str, Any]] = {}  # In-memory for testing
    
    @property
    def client(self):
        """Lazy load boto3 SQS client."""
        if self._client is None:
            try:
                import boto3
                self._client = boto3.client('sqs', region_name=self.region)
            except ImportError:
                self._client = None
        return self._client
    
    async def send_message(
        self,
        message_body: Dict[str, Any],
        delay_seconds: int = 0,
        message_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a message to the queue."""
        message_id = str(uuid.uuid4())
        
        message = {
            "message_id": message_id,
            "body": message_body,
            "delay_seconds": delay_seconds,
            "attributes": message_attributes or {},
            "sent_timestamp": datetime.utcnow().isoformat(),
            "receipt_handle": str(uuid.uuid4())
        }
        
        self._messages[message_id] = message
        
        if self.client:
            try:
                response = self.client.send_message(
                    QueueUrl=self.queue_url,
                    MessageBody=json.dumps(message_body),
                    DelaySeconds=delay_seconds,
                    MessageAttributes=self._format_attributes(message_attributes or {})
                )
                return {
                    "message_id": response.get("MessageId", message_id),
                    "success": True
                }
            except Exception as e:
                return {"message_id": message_id, "success": True, "local": True}
        
        return {"message_id": message_id, "success": True, "local": True}
    
    async def batch_send_messages(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Send multiple messages to the queue."""
        results = []
        for msg in messages:
            result = await self.send_message(msg)
            results.append(result)
        
        return {
            "successful": results,
            "failed": [],
            "total_sent": len(results)
        }
    
    async def receive_messages(
        self,
        max_messages: int = 10,
        wait_time_seconds: int = 0,
        visibility_timeout: int = 30
    ) -> List[Dict[str, Any]]:
        """Receive messages from the queue."""
        messages = list(self._messages.values())[:max_messages]
        
        if self.client:
            try:
                response = self.client.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=min(max_messages, 10),
                    WaitTimeSeconds=wait_time_seconds,
                    VisibilityTimeout=visibility_timeout
                )
                return response.get("Messages", messages)
            except Exception:
                pass
        
        return messages
    
    async def delete_message(self, receipt_handle: str) -> bool:
        """Delete a message from the queue."""
        # Remove from local storage
        for msg_id, msg in list(self._messages.items()):
            if msg.get("receipt_handle") == receipt_handle:
                del self._messages[msg_id]
                break
        
        if self.client:
            try:
                self.client.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=receipt_handle
                )
            except Exception:
                pass
        
        return True
    
    async def get_queue_attributes(self) -> Dict[str, Any]:
        """Get queue attributes."""
        attributes = {
            "ApproximateNumberOfMessages": str(len(self._messages)),
            "ApproximateNumberOfMessagesNotVisible": "0",
            "ApproximateNumberOfMessagesDelayed": "0",
            "QueueArn": f"arn:aws:sqs:{self.region}:123456789:ai-film-studio-queue"
        }
        
        if self.client:
            try:
                response = self.client.get_queue_attributes(
                    QueueUrl=self.queue_url,
                    AttributeNames=["All"]
                )
                return response.get("Attributes", attributes)
            except Exception:
                pass
        
        return attributes
    
    async def purge_queue(self) -> bool:
        """Purge all messages from the queue."""
        self._messages.clear()
        
        if self.client:
            try:
                self.client.purge_queue(QueueUrl=self.queue_url)
            except Exception:
                pass
        
        return True
    
    def _format_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Format message attributes for SQS."""
        formatted = {}
        for key, value in attributes.items():
            if isinstance(value, str):
                formatted[key] = {"DataType": "String", "StringValue": value}
            elif isinstance(value, (int, float)):
                formatted[key] = {"DataType": "Number", "StringValue": str(value)}
        return formatted


# Convenience instance
queue_service = QueueService()
