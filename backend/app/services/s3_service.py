"""
S3 service for file storage and signed URL generation.
"""
from datetime import datetime, timedelta
from typing import Optional
import boto3
from botocore.exceptions import ClientError

from ..core.config import settings


class S3Service:
    """Service for AWS S3 operations."""
    
    def __init__(self):
        """Initialize S3 client."""
        self.client = None
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        self.bucket_name = settings.S3_BUCKET_NAME
    
    def generate_signed_url(
        self,
        object_key: str,
        expiration: int = None
    ) -> tuple[Optional[str], Optional[datetime]]:
        """
        Generate a presigned URL for downloading an object.
        
        Args:
            object_key: S3 object key
            expiration: URL expiration time in seconds
        
        Returns:
            tuple: (signed_url, expires_at) or (None, None) if failed
        """
        if not self.client:
            # Return mock URL for development
            expires_at = datetime.utcnow() + timedelta(
                seconds=expiration or settings.S3_SIGNED_URL_EXPIRATION
            )
            return f"https://mock-s3-url.example.com/{object_key}", expires_at
        
        if expiration is None:
            expiration = settings.S3_SIGNED_URL_EXPIRATION
        
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
            expires_at = datetime.utcnow() + timedelta(seconds=expiration)
            return url, expires_at
        except ClientError as e:
            print(f"Error generating signed URL: {e}")
            return None, None
    
    def upload_file(
        self,
        file_path: str,
        object_key: str
    ) -> bool:
        """
        Upload a file to S3.
        
        Args:
            file_path: Local file path
            object_key: S3 object key
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            print(f"Mock upload: {file_path} -> {object_key}")
            return True
        
        try:
            self.client.upload_file(file_path, self.bucket_name, object_key)
            return True
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False
    
    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from S3.
        
        Args:
            object_key: S3 object key
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            print(f"Mock delete: {object_key}")
            return True
        
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError as e:
            print(f"Error deleting file: {e}")
            return False


# Global S3 service instance
s3_service = S3Service()
