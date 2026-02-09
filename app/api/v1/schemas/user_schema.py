from datetime import datetime
from pydantic import UUID7, BaseModel, EmailStr, ConfigDict 
from app.domain.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    user_name: str
    password: str
    user_role: UserRole 

class UserResponse(BaseModel):
    uuid: UUID7
    email: EmailStr
    user_name: str
    user_role: str
    user_status: str
    created_at: datetime 
    updated_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
