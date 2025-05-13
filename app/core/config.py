import os
from dotenv import load_dotenv
import base64

load_dotenv()

class Settings:
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "3600")
    
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "")

settings = Settings()