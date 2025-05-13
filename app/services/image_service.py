from datetime import datetime

from bson import ObjectId
from app.services.s3_service import S3Service
from app.repositories.image_repo import ImageRepository
from app.core.security import (encrypt_metadata, decrypt_metadata)
from typing import List, Optional

class ImageService:
    def __init__(self, repo: ImageRepository, s3: S3Service):
        self.repo = repo
        self.s3 = s3

    async def upload(self, file_bytes: bytes, filename: str, metadata: dict, uploaded_by: str):
        s3_url = self.s3.upload_file(file_bytes, filename)
        encrypted_metadata = encrypt_metadata(metadata) if metadata else None

        image_doc = {
            "filename": filename,
            "s3_url": s3_url,
            "url": s3_url,
            "metadata": encrypted_metadata,
            "uploaded_by": uploaded_by,
            "created_at": datetime.utcnow()
        }

        image_id = await self.repo.create(image_doc)
        return { "id": image_id, "filename": filename, "s3_url": s3_url }
    
    async def get_images_by_email(
        self,
        email: str,
        filename: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[dict]:
        records = await self.repo.find_by_email(
            email=email,
            filename=filename,
            limit=limit,
            skip=skip
        )

        for r in records:
            encrypted = r.get("metadata")
            if encrypted and isinstance(encrypted, str):
                try:
                    r["metadata"] = decrypt_metadata(encrypted)
                except Exception as e:
                    r["metadata"] = {"error": "decryption failed"}
                    print(f"[WARN] Failed to decrypt metadata: {e}")

        return records
    
    async def delete_image_by_id(self, image_id: ObjectId, uploaded_by: str) -> bool:
        image = await self.repo.find_one(image_id, uploaded_by)
        if not image:
            return False
        
        if image.get("uploaded_by") != uploaded_by:
            print(f"[DENY] {uploaded_by} tried to delete image owned by {image.get('uploaded_by')}")
            return False

        filename = image.get("filename")
        deleted = await self.repo.delete_image(image_id, uploaded_by)

        if deleted and filename:
            try:
                self.s3.delete_file(filename)
            except Exception as e:
                print(f"[WARN] Failed to delete file on S3: {filename}, error: {e}")

        return deleted