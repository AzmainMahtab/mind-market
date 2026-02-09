from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Union
from uuid import UUID
from app.domain.user import User, UserRegistrationData, UserRole, UserStatus, UserUpdateData



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
    async def get_by_id_or_uuid(self, id:  UUID) -> Optional[User]:
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
    async def soft_delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    async def prune(self, id: UUID) -> bool:
        """Permanent hard delete"""
        pass


class UserService(ABC):
    """
    Service Interface for User Service 

    """
    @abstractmethod
    async def register_user(self, user_data:UserRegistrationData) -> User:
        """
        Register a new user with the provided data.
        """
        pass

    @abstractmethod
    async def update_user(self, update_data:UserUpdateData, id: UUID) -> User:
        """
        Update user data for the user identified by uuid.
        """
        pass

    @abstractmethod
    async def get_user(self, id: UUID) -> Optional[User]:
        """
        Get user by uuid.
        """
        pass

    @abstractmethod
    async def list_users(self,
        skip: int = 0, 
        limit: int = 10, 
        role: Optional[UserRole] = None,
        status: Optional[UserStatus] = None
    ) -> Tuple[List[User], int]:
        """
        List users with pagination and optional filtering by role and status.
        Returns a tuple of (users_list, total_count)
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        """
        pass

    @abstractmethod
    async def soft_delete_user(self, id: UUID) -> bool:
        """
        Soft delete user by uuid.
        """
        pass
    
