"""
Cloudflare R2 Storage Service
Handles image uploads to Cloudflare R2 (S3-compatible storage)
"""
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import uuid
import os
from typing import Optional, Tuple
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class R2StorageService:
    """Service for managing Cloudflare R2 storage operations"""
    
    def __init__(self):
        """Initialize R2 client with credentials"""
        self.account_id = settings.R2_ACCOUNT_ID
        self.bucket_name = settings.R2_BUCKET_NAME
        
        # Initialize S3-compatible client for R2
        self.s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
            region_name='auto'
        )
        
        logger.info(f"R2 Storage Service initialized for bucket: {self.bucket_name}")
    
    def upload_image(
        self, 
        file_content: bytes, 
        filename: str, 
        folder: str = "images",
        content_type: str = "image/jpeg"
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Upload image to R2 storage
        
        Args:
            file_content: Binary content of the file
            filename: Original filename
            folder: Folder/prefix in R2 bucket (e.g., 'images', 'logos', 'priests')
            content_type: MIME type of the file
            
        Returns:
            Tuple of (success, url, error_message)
        """
        try:
            # Get file extension
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            
            # Create object key with folder structure
            object_key = f"{folder}/{unique_filename}"
            
            # Upload to R2 (R2 doesn't support ACL, uses bucket-level permissions)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type
            )
            
            # Construct public URL using R2 public dev URL
            public_url = f"{settings.R2_PUBLIC_URL}/{object_key}"
            
            logger.info(f"Successfully uploaded {object_key} to R2")
            return True, public_url, None
            
        except ClientError as e:
            error_msg = f"R2 upload failed: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = f"Unexpected error during R2 upload: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    def delete_image(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Delete image from R2 storage
        
        Args:
            url: Full URL of the image to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Extract object key from URL
            # URL format: https://pub-xxx.r2.dev/{key}
            base_url = settings.R2_PUBLIC_URL.rstrip("/")
            if not url.startswith(base_url):
                return False, "Invalid R2 URL format"
            
            object_key = url[len(base_url) + 1:]  # strip base + leading slash
            
            # Delete from R2
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            
            logger.info(f"Successfully deleted {object_key} from R2")
            return True, None
            
        except ClientError as e:
            error_msg = f"R2 delete failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during R2 delete: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def check_bucket_exists(self) -> bool:
        """Check if the R2 bucket exists and is accessible"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            return False

# Singleton instance
_r2_service = None

def get_r2_service() -> R2StorageService:
    """Get or create R2 storage service instance"""
    global _r2_service
    if _r2_service is None:
        _r2_service = R2StorageService()
    return _r2_service
