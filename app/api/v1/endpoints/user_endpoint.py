from app.api.v1.schemas.user_schema import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException
from app.ports.user_ports import UserService
from app.domain.user import User, UserRegistrationData
from app.api.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    req: UserCreate,
    service: UserService = Depends(get_user_service)
):
    user_data = UserRegistrationData(
        user_name=req.user_name,
        email=req.email,
        phone=req.phone,
        password=req.password,
        user_role=req.user_role
    )
    user = await service.register_user(
        user_data
    )
    if not user:
        raise HTTPException(status_code=400, detail="User registration failed")
    return user
