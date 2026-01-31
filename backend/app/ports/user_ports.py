from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Union
from uuid import UUID
from app.domain.user import User, UserRole, UserStatus



class UserRepository(ABC):
    """
    Repository interface for User entity.

    """
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id_or_uuid(self, identifier: Union[int, UUID]) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def list_users(
        self,
        skip: int = 0, 
        limit: int = 10, 
        role: Optional[UserRole] = None,
        status: Optional[UserStatus] = None
    ) -> Tuple[List[User], int]:
        """Returns a tuple of (users_list, total_count)"""
        pass

    @abstractmethod
    async def soft_delete(self, identifier: Union[int, UUID]) -> bool:
        pass

    @abstractmethod
    async def prune(self, identifier: Union[int, UUID]) -> bool:
        """Permanent hard delete"""
        pass
