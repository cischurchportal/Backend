"""
Cloudflare R2 Storage Service
Handles image uploads to Cloudflare R2 (S3-compatible storage)
"""
import boto3
import asyncio
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
        self.account_id = settings.R2_ACCOUNT_ID
        self.bucket_name = settings.R2_BUCKET_NAME
        self._client = None  # lazy — created on first use

    def _get_client(self):
        """Create boto3 client once and reuse (lazy init)."""
        if self._client is None:
            self._client = boto3.client(
                's3',
                endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                config=Config(
                    signature_version='s3v4',
                    connect_timeout=10,
                    read_timeout=30,
                    retries={'max_attempts': 2}
                ),
                region_name='auto'
            )
            logger.info(f"R2 client created for bucket: {self.bucket_name}")
        return self._client

    def _upload_sync(
        self,
        file_content: bytes,
        filename: str,
        folder: str,
        content_type: str
    ) -> Tuple[bool, str, Optional[str]]:
        """Synchronous upload — runs in thread pool."""
        try:
            file_ext = os.path.splitext(filename)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            object_key = f"{folder}/{unique_filename}"

            self._get_client().put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type
            )

            public_url = f"{settings.R2_PUBLIC_URL.rstrip('/')}/{object_key}"
            logger.info(f"Uploaded {object_key} to R2")
            return True, public_url, None

        except ClientError as e:
            error_msg = f"R2 upload failed: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = f"Unexpected R2 error: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg

    async def upload_image(
        self,
        file_content: bytes,
        filename: str,
        folder: str = "images",
        content_type: str = "image/jpeg"
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Upload image to R2 asynchronously (runs boto3 in thread pool
        so it doesn't block the FastAPI event loop).
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._upload_sync,
            file_content,
            filename,
            folder,
            content_type
        )

    def _delete_sync(self, url: str) -> Tuple[bool, Optional[str]]:
        """Synchronous delete — runs in thread pool."""
        try:
            base_url = settings.R2_PUBLIC_URL.rstrip("/")
            if not url.startswith(base_url):
                return False, "Invalid R2 URL format"
            object_key = url[len(base_url) + 1:]
            self._get_client().delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info(f"Deleted {object_key} from R2")
            return True, None
        except ClientError as e:
            return False, f"R2 delete failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected R2 error: {str(e)}"

    async def delete_image(self, url: str) -> Tuple[bool, Optional[str]]:
        """Delete image from R2 asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._delete_sync, url)

    def check_bucket_exists(self) -> bool:
        try:
            self._get_client().head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            return False


# Singleton
_r2_service = None

def get_r2_service() -> R2StorageService:
    global _r2_service
    if _r2_service is None:
        _r2_service = R2StorageService()
    return _r2_service
