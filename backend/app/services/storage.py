from datetime import timedelta
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings


class StorageService:
    """Service for managing asset storage and signed URLs"""
    
    def __init__(self):
        self.bucket_name = settings.S3_BUCKET_NAME
        self.region = settings.AWS_REGION
        self.expiration = settings.S3_PRESIGNED_URL_EXPIRATION
        
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=self.region
            )
        else:
            self.s3_client = None
    
    def generate_presigned_url(
        self,
        object_key: str,
        operation: str = "get_object",
        expiration: Optional[int] = None
    ) -> Optional[str]:
        """
        Generate a presigned URL for an S3 object
        
        Args:
            object_key: The S3 object key
            operation: The S3 operation (get_object, put_object, etc.)
            expiration: URL expiration time in seconds
            
        Returns:
            Presigned URL or None if S3 is not configured
        """
        if not self.s3_client or not self.bucket_name:
            # Return a mock URL for development
            return f"https://storage.example.com/{object_key}"
        
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod=operation,
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration or self.expiration
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def generate_upload_url(self, object_key: str) -> Optional[str]:
        """Generate a presigned URL for uploading an object"""
        return self.generate_presigned_url(object_key, operation="put_object")
    
    def generate_download_url(self, object_key: str) -> Optional[str]:
        """Generate a presigned URL for downloading an object"""
        return self.generate_presigned_url(object_key, operation="get_object")


storage_service = StorageService()
