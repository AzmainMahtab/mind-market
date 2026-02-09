from typing import Optional, List, Tuple
from uuid import UUID

from app.domain.user import User, UserRegistrationData, UserUpdateData, UserRole, UserStatus
from app.ports.user_ports import UserService, UserRepository
from app.ports.hash_port import HashPort

class UserServiceImpl(UserService):
    def __init__(self, user_repo: UserRepository, hasher: HashPort):
        self.user_repo = user_repo
        self.hasher = hasher

    async def register_user(self, user_data: UserRegistrationData) -> User:
        # Check for existing user
        if await self.user_repo.get_by_email(user_data.email):
            raise ValueError(f"User with email {user_data.email} already exists")
        
        if await self.user_repo.get_by_username(user_data.user_name):
            raise ValueError(f"Username {user_data.user_name} is already taken")

        # Hash password via injected port
        hashed_password = self.hasher.hash(user_data.password)

        # Create Domain Entity (ID 0/None because it's not in DB yet)
        new_user = User(
            id=0, 
            user_name=user_data.user_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            user_status=UserStatus.ACTIVE,
            user_role=user_data.user_role
        )

        return await self.user_repo.create(new_user)

    async def update_user(self, update_data: UserUpdateData, id: UUID) -> User:
        user = await self.user_repo.get_by_id_or_uuid(id)
        if not user:
            raise ValueError("User not found")

        # Update only provided fields
        if update_data.user_name is not None:
            user.user_name = update_data.user_name
        if update_data.phone is not None:
            user.phone = update_data.phone

        return await self.user_repo.update(user)

    async def get_user(self, id: UUID) -> Optional[User]:
        return await self.user_repo.get_by_id_or_uuid(id)

    async def list_users(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        role: Optional[UserRole] = None, 
        status: Optional[UserStatus] = None
    ) -> Tuple[List[User], int]:
        return await self.user_repo.list_users(skip, limit, role, status)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repo.get_by_email(email)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.user_repo.get_by_username(username)

    async def soft_delete_user(self, id: UUID) -> bool:
        return await self.user_repo.soft_delete(id)
