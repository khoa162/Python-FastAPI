from fastapi import Request, Depends, HTTPException, status
from app.services.image_service import ImageService
from app.core.jwt_utils import verify_access_token
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.repositories.user_repo import UserRepository
from app.repositories.image_repo import ImageRepository

def get_image_service(request: Request) -> ImageService:
    return request.app.container.image_service()

def get_user_service(request: Request):
    return request.app.container.user_service()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = verify_access_token(token)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_repository(request: Request) -> UserRepository:
    return request.app.container.user_repository()

def get_user_repository(request: Request) -> UserRepository:
    return request.app.container.user_repository()