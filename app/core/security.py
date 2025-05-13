from passlib.context import CryptContext
from cryptography.fernet import Fernet
from app.core.config import settings
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def encrypt_metadata(data: dict) -> str:
    if not isinstance(data, dict):
        raise ValueError("metadata must be a dictionary")
    json_text = json.dumps(data)
    return fernet.encrypt(json_text.encode()).decode()

def decrypt_metadata(token: str) -> dict:
    decrypted = fernet.decrypt(token.encode()).decode()
    return json.loads(decrypted)