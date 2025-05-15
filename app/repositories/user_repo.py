from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user_model import UserModel
from bson import ObjectId

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def create(self, user: UserModel) -> str:
        user_dict = user.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(user_dict)
        return str(result.inserted_id)

    async def find_by_email(self, email: str) -> UserModel | None:
        doc = await self.collection.find_one({"email": email})
        if doc:
            doc["id"] = doc.pop("_id")
            return UserModel.model_validate(doc)
        return None