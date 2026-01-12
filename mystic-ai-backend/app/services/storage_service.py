"""
Storage Service - Upload files to S3 or local storage
"""

import boto3
from botocore.exceptions import ClientError
import uuid
import logging
from typing import Optional
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Service for uploading and managing files"""

    def __init__(self):
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            # AWS S3 client
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.use_s3 = True
            self.bucket_name = settings.S3_BUCKET_NAME
        else:
            # Local storage fallback
            self.use_s3 = False
            self.upload_dir = Path("uploads")
            self.upload_dir.mkdir(exist_ok=True)
            logger.warning("AWS credentials not found, using local storage")

    def upload_image(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        user_id: int,
        image_type: str = "reading"
    ) -> str:
        """
        Upload an image file

        Args:
            file_content: File binary content
            filename: Original filename
            content_type: MIME type (image/jpeg, image/png, etc.)
            user_id: User ID for organization
            image_type: Type of image (reading, profile, etc.)

        Returns:
            Public URL of uploaded file
        """
        # Generate unique filename
        file_ext = Path(filename).suffix.lower()
        unique_filename = f"{user_id}/{image_type}/{uuid.uuid4()}{file_ext}"

        if self.use_s3:
            return self._upload_to_s3(
                file_content=file_content,
                key=unique_filename,
                content_type=content_type
            )
        else:
            return self._upload_to_local(
                file_content=file_content,
                filename=unique_filename
            )

    def _upload_to_s3(
        self,
        file_content: bytes,
        key: str,
        content_type: str
    ) -> str:
        """Upload to AWS S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_content,
                ContentType=content_type,
                ACL='public-read'  # Make publicly accessible
            )

            # Construct public URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

            logger.info(f"Uploaded to S3: {url}")
            return url

        except ClientError as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise Exception(f"Failed to upload image: {str(e)}")

    def _upload_to_local(
        self,
        file_content: bytes,
        filename: str
    ) -> str:
        """Upload to local filesystem (development)"""
        file_path = self.upload_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Return local URL (in production, use proper domain)
        url = f"http://localhost:8000/uploads/{filename}"

        logger.info(f"Uploaded locally: {url}")
        return url

    def delete_image(self, url: str) -> bool:
        """
        Delete an image

        Args:
            url: Image URL

        Returns:
            True if successful, False otherwise
        """
        if self.use_s3:
            return self._delete_from_s3(url)
        else:
            return self._delete_from_local(url)

    def _delete_from_s3(self, url: str) -> bool:
        """Delete from S3"""
        try:
            # Extract key from URL
            key = url.split(f"{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/")[1]

            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )

            logger.info(f"Deleted from S3: {key}")
            return True

        except Exception as e:
            logger.error(f"S3 deletion failed: {str(e)}")
            return False

    def _delete_from_local(self, url: str) -> bool:
        """Delete from local filesystem"""
        try:
            # Extract filename from URL
            filename = url.split("/uploads/")[1]
            file_path = self.upload_dir / filename

            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted locally: {filename}")
                return True

            return False

        except Exception as e:
            logger.error(f"Local deletion failed: {str(e)}")
            return False

    def get_presigned_url(self, key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for temporary access (S3 only)

        Args:
            key: S3 object key
            expiration: URL expiration in seconds (default: 1 hour)

        Returns:
            Presigned URL or None
        """
        if not self.use_s3:
            return None

        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': key
                },
                ExpiresIn=expiration
            )

            return url

        except ClientError as e:
            logger.error(f"Presigned URL generation failed: {str(e)}")
            return None
