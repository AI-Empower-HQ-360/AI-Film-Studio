"""
S3 Storage Service
Handles file upload, download, and management in S3
"""
import os
import asyncio
import logging
from typing import Optional, Dict, Any, List, AsyncIterator
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
    ClientError = Exception

logger = logging.getLogger(__name__)


class S3Service:
    """Service for S3 storage operations"""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize S3 service
        
        Args:
            region: AWS region
        """
        self.region = region
        if HAS_BOTO3:
            self.client = boto3.client("s3", region_name=region)
        else:
            self.client = None
    
    async def upload_video(
        self,
        file_path: str,
        key: str,
        bucket: str,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Upload video file to S3
        
        Args:
            file_path: Local file path
            key: S3 object key
            bucket: S3 bucket name
            metadata: Optional metadata dictionary
            **kwargs: Additional upload parameters
            
        Returns:
            Upload result with ETag and other metadata
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            # Convert metadata to S3 format
            s3_metadata = {}
            if metadata:
                for k, v in metadata.items():
                    s3_metadata[f"x-amz-meta-{k}"] = str(v)
            
            # Read file
            with open(file_path, "rb") as f:
                file_data = f.read()
            
            # Upload to S3
            response = self.client.put_object(
                Bucket=bucket,
                Key=key,
                Body=file_data,
                Metadata=s3_metadata if s3_metadata else None,
                **kwargs
            )
            
            return {
                "ETag": response.get("ETag", ""),
                "key": key,
                "bucket": bucket,
                "size": len(file_data)
            }
            
        except Exception as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            raise
    
    async def upload_large_file(
        self,
        file_path: str,
        key: str,
        bucket: str,
        part_size: int = 5 * 1024 * 1024,  # 5MB default
        **kwargs
    ) -> Dict[str, Any]:
        """
        Upload large file using multipart upload
        
        Args:
            file_path: Local file path
            key: S3 object key
            bucket: S3 bucket name
            part_size: Size of each part in bytes
            **kwargs: Additional upload parameters
            
        Returns:
            Upload result
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            # Initiate multipart upload
            response = self.client.create_multipart_upload(
                Bucket=bucket,
                Key=key,
                **kwargs
            )
            upload_id = response["UploadId"]
            
            # Upload parts
            parts = []
            part_number = 1
            
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(part_size)
                    if not chunk:
                        break
                    
                    part_response = self.client.upload_part(
                        Bucket=bucket,
                        Key=key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=chunk
                    )
                    
                    parts.append({
                        "ETag": part_response["ETag"],
                        "PartNumber": part_number
                    })
                    part_number += 1
            
            # Complete multipart upload
            complete_response = self.client.complete_multipart_upload(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts}
            )
            
            return {
                "Location": complete_response.get("Location", ""),
                "key": key,
                "bucket": bucket,
                "upload_id": upload_id
            }
            
        except Exception as e:
            logger.error(f"Error in multipart upload: {str(e)}")
            # Abort upload on error
            try:
                self.client.abort_multipart_upload(
                    Bucket=bucket,
                    Key=key,
                    UploadId=upload_id
                )
            except:
                pass
            raise
    
    async def download(
        self,
        key: str,
        bucket: str,
        destination: str,
        **kwargs
    ) -> str:
        """
        Download file from S3
        
        Args:
            key: S3 object key
            bucket: S3 bucket name
            destination: Local destination path
            **kwargs: Additional download parameters
            
        Returns:
            Path to downloaded file
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(destination) if os.path.dirname(destination) else ".", exist_ok=True)
            
            # Download file
            self.client.download_file(
                Bucket=bucket,
                Key=key,
                Filename=destination,
                **kwargs
            )
            
            return destination
            
        except Exception as e:
            logger.error(f"Error downloading file from S3: {str(e)}")
            raise
    
    async def get_presigned_url(
        self,
        key: str,
        bucket: str,
        expiration: int = 3600,
        **kwargs
    ) -> str:
        """
        Generate presigned URL for S3 object
        
        Args:
            key: S3 object key
            bucket: S3 bucket name
            expiration: URL expiration time in seconds
            **kwargs: Additional parameters
            
        Returns:
            Presigned URL
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiration,
                **kwargs
            )
            return url
            
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            raise
    
    async def stream_download(
        self,
        key: str,
        bucket: str,
        **kwargs
    ) -> AsyncIterator[bytes]:
        """
        Stream download for large files
        
        Args:
            key: S3 object key
            bucket: S3 bucket name
            **kwargs: Additional parameters
            
        Yields:
            Chunks of file data
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            response = self.client.get_object(
                Bucket=bucket,
                Key=key,
                **kwargs
            )
            
            body = response["Body"]
            
            # Stream chunks
            for chunk in body.iter_chunks():
                yield chunk
                
        except Exception as e:
            logger.error(f"Error streaming download: {str(e)}")
            raise
    
    async def list_objects(
        self,
        bucket: str,
        prefix: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        List objects in bucket
        
        Args:
            bucket: S3 bucket name
            prefix: Optional key prefix filter
            **kwargs: Additional parameters
            
        Returns:
            List of object metadata dictionaries
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            params = {"Bucket": bucket}
            if prefix:
                params["Prefix"] = prefix
            
            response = self.client.list_objects_v2(**params, **kwargs)
            
            objects = []
            if "Contents" in response:
                for obj in response["Contents"]:
                    objects.append({
                        "Key": obj["Key"],
                        "Size": obj["Size"],
                        "LastModified": obj["LastModified"].isoformat() if hasattr(obj["LastModified"], "isoformat") else str(obj["LastModified"]),
                        "ETag": obj.get("ETag", "")
                    })
            
            return objects
            
        except Exception as e:
            logger.error(f"Error listing objects: {str(e)}")
            raise
    
    async def delete(
        self,
        key: str,
        bucket: str,
        **kwargs
    ) -> bool:
        """
        Delete object from S3
        
        Args:
            key: S3 object key
            bucket: S3 bucket name
            **kwargs: Additional parameters
            
        Returns:
            True if successful
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            self.client.delete_object(
                Bucket=bucket,
                Key=key,
                **kwargs
            )
            return True
            
        except Exception as e:
            logger.error(f"Error deleting object: {str(e)}")
            raise
    
    async def copy(
        self,
        source_key: str,
        dest_key: str,
        bucket: str,
        **kwargs
    ) -> bool:
        """
        Copy object within S3
        
        Args:
            source_key: Source object key
            dest_key: Destination object key
            bucket: S3 bucket name
            **kwargs: Additional parameters
            
        Returns:
            True if successful
        """
        if not self.client:
            raise ValueError("S3 client not initialized")
        
        try:
            copy_source = {"Bucket": bucket, "Key": source_key}
            
            self.client.copy_object(
                CopySource=copy_source,
                Bucket=bucket,
                Key=dest_key,
                **kwargs
            )
            return True
            
        except Exception as e:
            logger.error(f"Error copying object: {str(e)}")
            raise
