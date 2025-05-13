from pydantic import BaseModel, Field
from typing import Optional, Dict
from bson import ObjectId

class ImageUploadRequest(BaseModel):
    filename: str = Field(..., min_length=1)
    metadata: Optional[Dict] = None
    uploaded_by: str = Field(..., min_length=5)

class ImageUploadResponse(BaseModel):
    id: str
    filename: str
    s3_url: str

class ImageRecord(BaseModel):
    id: str
    filename: str
    s3_url: str
    uploaded_by: str
    metadata: Optional[Dict] = None

class ImageQueryParams(BaseModel):
    filename: Optional[str] = Field(None, min_length=1)
    limit: int = Field(50, ge=1, le=100)
    page: int = Field(1, ge=1)