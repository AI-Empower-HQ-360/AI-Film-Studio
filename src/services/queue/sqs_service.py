"""
SQS Queue Service
Handles message queuing with AWS SQS
"""
import json
import asyncio
import logging
from typing import Optional, Dict, Any, List

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
    ClientError = Exception

logger = logging.getLogger(__name__)


class SQSService:
    """Service for SQS queue operations"""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize SQS service
        
        Args:
            region: AWS region
        """
        self.region = region
        if HAS_BOTO3:
            self.client = boto3.client("sqs", region_name=region)
        else:
            self.client = None
    
    async def send_message(
        self,
        queue_url: str,
        message: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send message to SQS queue
        
        Args:
            queue_url: SQS queue URL
            message: Message dictionary
            **kwargs: Additional parameters
            
        Returns:
            Response with MessageId
        """
        if not self.client:
            raise ValueError("SQS client not initialized")
        
        try:
            response = self.client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message),
                **kwargs
            )
            return response
            
        except Exception as e:
            logger.error(f"Error sending message to SQS: {str(e)}")
            raise
    
    async def receive_messages(
        self,
        queue_url: str,
        max_messages: int = 10,
        wait_time: int = 20,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Receive messages from SQS queue
        
        Args:
            queue_url: SQS queue URL
            max_messages: Maximum number of messages to receive
            wait_time: Long polling wait time in seconds
            **kwargs: Additional parameters
            
        Returns:
            List of message dictionaries
        """
        if not self.client:
            raise ValueError("SQS client not initialized")
        
        try:
            response = self.client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=min(max_messages, 10),  # SQS limit
                WaitTimeSeconds=wait_time,
                **kwargs
            )
            
            messages = []
            if "Messages" in response:
                for msg in response["Messages"]:
                    try:
                        body = json.loads(msg["Body"])
                    except json.JSONDecodeError:
                        body = msg["Body"]
                    
                    messages.append({
                        "MessageId": msg["MessageId"],
                        "Body": body,
                        "ReceiptHandle": msg["ReceiptHandle"],
                        "Attributes": msg.get("Attributes", {})
                    })
            
            return messages
            
        except Exception as e:
            logger.error(f"Error receiving messages from SQS: {str(e)}")
            raise
    
    async def delete_message(
        self,
        queue_url: str,
        receipt_handle: str,
        **kwargs
    ) -> bool:
        """
        Delete message from queue after processing
        
        Args:
            queue_url: SQS queue URL
            receipt_handle: Message receipt handle
            **kwargs: Additional parameters
            
        Returns:
            True if successful
        """
        if not self.client:
            raise ValueError("SQS client not initialized")
        
        try:
            self.client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle,
                **kwargs
            )
            return True
            
        except Exception as e:
            logger.error(f"Error deleting message from SQS: {str(e)}")
            raise
    
    async def send_batch(
        self,
        queue_url: str,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send batch of messages to SQS queue
        
        Args:
            queue_url: SQS queue URL
            messages: List of message dictionaries
            **kwargs: Additional parameters
            
        Returns:
            Response with Successful and Failed lists
        """
        if not self.client:
            raise ValueError("SQS client not initialized")
        
        try:
            # Prepare entries (max 10 per batch)
            entries = []
            for i, msg in enumerate(messages[:10]):  # SQS batch limit
                entries.append({
                    "Id": str(i),
                    "MessageBody": json.dumps(msg)
                })
            
            response = self.client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries,
                **kwargs
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending batch to SQS: {str(e)}")
            raise
    
    async def get_queue_stats(
        self,
        queue_url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get queue statistics
        
        Args:
            queue_url: SQS queue URL
            **kwargs: Additional parameters
            
        Returns:
            Queue attributes dictionary
        """
        if not self.client:
            raise ValueError("SQS client not initialized")
        
        try:
            response = self.client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=["All"],
                **kwargs
            )
            
            return response.get("Attributes", {})
            
        except Exception as e:
            logger.error(f"Error getting queue stats: {str(e)}")
            raise
    
    async def purge(
        self,
        queue_url: str,
        **kwargs
    ) -> bool:
        """
        Purge all messages from queue
        
        Args:
            queue_url: SQS queue URL
            **kwargs: Additional parameters
            
        Returns:
            True if successful
        """
        if not self.client:
            raise ValueError("SQS client not initialized")
        
        try:
            self.client.purge_queue(
                QueueUrl=queue_url,
                **kwargs
            )
            return True
            
        except Exception as e:
            logger.error(f"Error purging queue: {str(e)}")
            raise
