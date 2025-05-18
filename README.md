# 📸 Image Gallery API

FastAPI backend for uploading images to AWS S3, storing encrypted metadata in MongoDB, and retrieving images securely via JWT.

## ✅ Features
- Fundamental Signup and Login 
- Upload image to AWS S3
- Store encrypted metadata in MongoDB
- Retrieve images of the authenticated user (`/images/my-images`)
- Filter by filename, paginate with `limit` and `page`
- JWT-based auth
- Encryption via Fernet
- Dependency Injection with `dependency-injector`

## 🗄️ MongoDB Setup (Docker)

MongoDB is included via `docker-compose`.

To start:
```bash
docker-compose up -d
```
This will start a local MongoDB instance on `mongodb://localhost:27017/image_gallery`

## 🛠 Setup

```bash
git clone <your-repo>
cd image_gallery
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Swagger
http://localhost:8000/docs


### .env file

```env
MONGODB_URL=mongodb://localhost:27017/image_gallery
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET_NAME=your_bucket
ENCRYPTION_KEY=your_fernet_key
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

### 🧩 Fixing .env Issues

If you get errors like `InvalidURI` or `Fernet key must be 32 url-safe base64-encoded bytes`, fix your `.env` like this:

```env
# ✅ MongoDB connection URI (required)
MONGODB_URL=mongodb://localhost:27017/image_gallery

# ✅ Fernet encryption key (must be base64, 32 bytes)
# Generate with: python scripts/gen_key.py
ENCRYPTION_KEY=XxL1qP9V4F-8R8o6fQsYoY0-H7u4ksTfYQOpxEplZX0=

Or define it inside `.env`.

## 🚀 Run the server

```bash
uvicorn app.main:app --reload
```

Make sure:
- MongoDB is running
- `.env` is loaded (via Pydantic `BaseSettings`)
- AWS credentials are valid

### Fixing MONGO_URL in .env
If you have any problems with MONGO_URL, please run export MONGODB_URL=mongodb://localhost:27017/image_gallery

## 🔐 Auth (JWT)

All secured routes require:

```
Authorization: Bearer <your_token>
```

JWT token must contain:

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1747065825
}
```

`email` is used to query Mongo (uploaded_by)

## 🔎 API Endpoints

| Method | Route                 | Description                          |
|--------|------------------------|--------------------------------------|
| POST   | /images/upload         | Upload image + metadata              |
| GET    | /images/my-images      | Get current user's images (JWT)      |

Optional query params for `/images/my-images`:
- `filename=abc.jpg`
- `limit=10` (default 50, max 100)
- `page=2` (default 1)

## 📂 Project Structure

```
app/
├── api/routes/image.py
├── schemas/image_schema.py
├── services/image_service.py
├── repositories/image_repo.py
├── containers.py
├── core/security.py
└── main.py
```

## 🧪 Demo Environment (for quick testing)

This project includes a preconfigured `.env` file for quick testing.

⚠️ The included `.env` uses shared AWS S3 credentials with restricted permissions:
- For demo/testing purposes only
- Do not upload sensitive or large files
- The S3 bucket may be closed or rotated after **7 days**
- Abuse may result in access being revoked without notice

If you prefer full control, copy `.env.example` and configure your own AWS credentials.

## ⚠️ Security Note

This project includes a `.env` file **only for demo/testing purposes**.  
In real production environments:

- **Do not commit `.env` to Git**
- **Do not expose AWS keys, JWT secrets, or encryption keys in source code**
- Use environment variables or a secure secret management system (e.g. AWS Secrets Manager)
- Always rotate and limit credentials used for testing

The included `.env` is safe for local testing, but should **never be used in production** as-is.