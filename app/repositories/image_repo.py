from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional

class ImageRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["images"]

    async def create(self, image: dict) -> str:
        result = await self.collection.insert_one(image)
        return str(result.inserted_id)
    
    async def find_by_email(
        self,
        email: str,
        filename: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[dict]:
        query = {"uploaded_by": email}
        if filename:
            query["filename"] = filename

        cursor = self.collection.find(query).skip(skip).limit(limit)
        records = await cursor.to_list(length=limit)

        for r in records:
            r["id"] = str(r["_id"])
            del r["_id"]
        return records
    
    async def delete_image(self, image_id: ObjectId, uploaded_by: str) -> bool:
        result = await self.collection.delete_one({
            "_id": image_id,
            "uploaded_by": uploaded_by
        })
        return result.deleted_count == 1
    
    async def find_one(self, image_id: ObjectId, uploaded_by: str) -> Optional[dict]:
        doc = await self.collection.find_one({
            "_id": image_id,
            "uploaded_by": uploaded_by
        })
        return doc