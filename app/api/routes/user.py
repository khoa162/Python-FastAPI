from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.user_schema import UserCreate, UserLogin, UserOut, UserLoginResponse
from app.services.user_service import UserService
from app.api.deps import get_user_service
from app.core.jwt_utils import create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserOut)
async def signup(request: Request, user_in: UserCreate, service: UserService = Depends(get_user_service)):
    logger = request.app.state.logger
    try:
        user = await service.signup(user_in)
        logger.info(f"[SIGNUP] New user registered: {user['email']}")
        return user
    except ValueError as e:
        logger.warning(f"[SIGNUP] Registration failed for {user_in.email}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[SIGNUP] Unexpected error for {user_in.email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during signup")

@router.post("/login", response_model=UserLoginResponse)
async def login(request: Request, data: UserLogin, service: UserService = Depends(get_user_service)):
    logger = request.app.state.logger
    try:
        user = await service.login(data)
        token = create_access_token({"sub": user["id"], "email": user["email"]})
        logger.info(f"[LOGIN] Successful login: {user['email']}")
        return {
            "access_token": token,
            "user": user
        }
    except ValueError:
        logger.warning(f"[LOGIN] Failed login attempt: {data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"[LOGIN] Unexpected error for {data.email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during login")