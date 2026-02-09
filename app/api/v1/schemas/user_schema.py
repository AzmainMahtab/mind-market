from pydantic import UUID7, BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str

class UserResponse(BaseModel):
    uuid: UUID7
    email: EmailStr
    user_name: str
    user_role: str
    user_status: str
    created_at: str
    updated_at: str
    deleted_at: str | None

    model_config = ConfigDict(from_attributes=True)
