from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

class ImageModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    filename: str
    s3_url: str
    url: Optional[str] = None
    uploaded_by: ObjectId
    metadata: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }