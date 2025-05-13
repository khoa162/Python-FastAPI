from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user_model import UserModel
from bson import ObjectId

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def create(self, user: dict) -> str:
        result = await self.collection.insert_one(user)
        return str(result.inserted_id)

    async def find_by_email(self, email: str) -> dict:
        return await self.collection.find_one({"email": email})