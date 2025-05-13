from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self, s3_client: Session):
        self.s3 = s3_client
        self.bucket = settings.S3_BUCKET

    def upload_file(self, file_bytes: bytes, key: str, content_type: str = "image/jpeg") -> str:
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_bytes,
                ContentType=content_type
            )
            url = f"https://{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
            return url
        except (BotoCoreError, ClientError) as e:
            logger.error(f" Failed to upload to S3: {e}")
            raise

    def delete_file(self, key: str):
        try:
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=key
            )
            logger.info(f" Deleted file from S3: {key}")
        except (BotoCoreError, ClientError) as e:
            logger.warning(f" Failed to delete from S3: {key} | Error: {e}")