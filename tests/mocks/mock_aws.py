"""Mock AWS services for testing"""

import boto3
from moto import mock_s3, mock_sqs


class MockS3Service:
    """Mock S3 service for testing"""

    def __init__(self, bucket_name="test-bucket"):
        self.bucket_name = bucket_name
        self.mock = mock_s3()

    def __enter__(self):
        """Start mock S3 service"""
        self.mock.start()

        # Create S3 client and bucket
        self.client = boto3.client("s3", region_name="us-east-1")
        self.client.create_bucket(Bucket=self.bucket_name)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop mock S3 service"""
        self.mock.stop()

    def upload_file(self, key, content):
        """Upload file to mock S3"""
        self.client.put_object(Bucket=self.bucket_name, Key=key, Body=content)

    def download_file(self, key):
        """Download file from mock S3"""
        response = self.client.get_object(Bucket=self.bucket_name, Key=key)
        return response["Body"].read()

    def delete_file(self, key):
        """Delete file from mock S3"""
        self.client.delete_object(Bucket=self.bucket_name, Key=key)

    def list_files(self, prefix=""):
        """List files in mock S3"""
        response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]


class MockSQSService:
    """Mock SQS service for testing"""

    def __init__(self, queue_name="test-queue"):
        self.queue_name = queue_name
        self.mock = mock_sqs()

    def __enter__(self):
        """Start mock SQS service"""
        self.mock.start()

        # Create SQS client and queue
        self.client = boto3.client("sqs", region_name="us-east-1")
        response = self.client.create_queue(QueueName=self.queue_name)
        self.queue_url = response["QueueUrl"]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop mock SQS service"""
        self.mock.stop()

    def send_message(self, message_body, message_attributes=None):
        """Send message to mock SQS"""
        kwargs = {"QueueUrl": self.queue_url, "MessageBody": message_body}
        if message_attributes:
            kwargs["MessageAttributes"] = message_attributes

        return self.client.send_message(**kwargs)

    def receive_messages(self, max_messages=1, wait_time=0):
        """Receive messages from mock SQS"""
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
        )
        return response.get("Messages", [])

    def delete_message(self, receipt_handle):
        """Delete message from mock SQS"""
        self.client.delete_message(
            QueueUrl=self.queue_url, ReceiptHandle=receipt_handle
        )

    def get_queue_attributes(self):
        """Get queue attributes"""
        response = self.client.get_queue_attributes(
            QueueUrl=self.queue_url, AttributeNames=["All"]
        )
        return response["Attributes"]


# Example usage in tests:
# def test_s3_integration():
#     with MockS3Service() as s3:
#         s3.upload_file("test.txt", b"test content")
#         content = s3.download_file("test.txt")
#         assert content == b"test content"
#
# def test_sqs_integration():
#     with MockSQSService() as sqs:
#         sqs.send_message("test message")
#         messages = sqs.receive_messages()
#         assert len(messages) == 1
#         assert messages[0]["Body"] == "test message"
