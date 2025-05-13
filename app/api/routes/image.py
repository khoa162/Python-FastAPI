from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request
import json
from typing import Optional, List

from app.schemas.image_schema import (
    ImageUploadResponse,
    ImageRecord,
    ImageQueryParams
)
from app.services.image_service import ImageService
from app.repositories.user_repo import UserRepository
from app.api.deps import (
    get_image_service,
    get_user_repository,
    get_current_user
)

router = APIRouter()

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    filename: str = Form(...),
    metadata: Optional[str] = Form(None),
    service: ImageService = Depends(get_image_service),
    user: dict = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository)
):
    logger = request.app.state.logger

    if file.content_type not in ["image/jpeg", "image/png"]:
        logger.warning(f"[UPLOAD] Invalid content type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid image type")

    try:
        metadata_dict = json.loads(metadata) if metadata else {}
    except Exception as e:
        logger.warning(f"[UPLOAD] Failed to parse metadata: {e}")
        raise HTTPException(status_code=400, detail="Invalid metadata JSON")
    
    try:
        email = user.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token: missing email")

        user_in_db = await user_repo.find_by_email(email)
        if not user_in_db:
            logger.info(f"[UPLOAD] Uploader not found in DB: {email}")
            raise HTTPException(status_code=404, detail="Uploader email not found")

        file_bytes = await file.read()
        result = await service.upload(file_bytes, filename, metadata_dict, uploaded_by=email)
        logger.info(f"[UPLOAD] Uploaded image: {filename} by {email}")
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[UPLOAD] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during upload")

@router.get("/my-images", response_model=List[ImageRecord])
async def get_my_images(
    request: Request,
    query: ImageQueryParams = Depends(),
    service: ImageService = Depends(get_image_service),
    user: dict = Depends(get_current_user),
):
    logger = request.app.state.logger
    email = user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token: missing email")

    try:
        images = await service.get_images_by_email(
            email=email,
            filename=query.filename,
            limit=query.limit,
            skip=(query.page - 1) * query.limit
        )
    except Exception as e:
        logger.error(f"[GET MY IMAGES] Failed to fetch images for {email}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch images from database")

    if not images:
        logger.info(f"[GET MY IMAGES] No images found for {email}")
        raise HTTPException(status_code=404, detail="No images found")

    logger.info(f"[GET MY IMAGES] Returned {len(images)} images for {email}")
    return images

@router.delete("/{image_id}")
async def delete_image(
    request: Request,
    image_id: str,
    user: dict = Depends(get_current_user),
    service: ImageService = Depends(get_image_service)
):
    logger = request.app.state.logger
    email = user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token: missing email")

    try:
        obj_id = ObjectId(image_id)
    except Exception as e:
        logger.warning(f"[DELETE] Invalid ID format: {image_id} | Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid image ID format")

    try:
        deleted = await service.delete_image_by_id(image_id=obj_id, uploaded_by=email)
    except Exception as e:
        logger.error(f"[DELETE] Failed to delete image {image_id} by {email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while deleting image")

    if not deleted:
        logger.info(f"[DELETE] Not found or unauthorized: {image_id} by {email}")
        raise HTTPException(status_code=404, detail="Image not found or not owned by user")

    logger.info(f"[DELETE] Deleted image {image_id} by {email}")
    return {"message": "Image deleted successfully"}