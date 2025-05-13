from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def signup(self, data):
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise ValueError("Email already exists")

        user_dict = {
            "name": data.name,
            "email": data.email,
            "password": hash_password(data.password)
        }
        user_id = await self.repo.create(user_dict)
        return { "id": user_id, "name": data.name, "email": data.email }

    async def login(self, data):
        user = await self.repo.find_by_email(data.email)
        if not user or not verify_password(data.password, user["password"]):
            raise ValueError("Invalid credentials")

        return { "id": str(user["_id"]), "name": user["name"], "email": user["email"] }