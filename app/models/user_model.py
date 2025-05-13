from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    name: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }