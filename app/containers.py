from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.repositories.image_repo import ImageRepository
from app.services.image_service import ImageService
from app.services.s3_service import S3Service
from app.core.s3 import get_s3_client

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    mongo_client = providers.Singleton(AsyncIOMotorClient, settings.MONGODB_URL)
    db = providers.Resource(lambda mongo: mongo.get_default_database(), mongo=mongo_client)

    user_repository = providers.Factory(UserRepository, db=db)
    user_service = providers.Factory(UserService, repo=user_repository)
    
    s3_client = providers.Singleton(get_s3_client)
    s3_service = providers.Factory(S3Service, s3_client=s3_client)
    
    image_repository = providers.Factory(ImageRepository, db=db)
    image_service = providers.Factory(ImageService, repo=image_repository, s3=s3_service)
    