from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from dataclasses import dataclass, field
from datetime import datetime, timezone

class UserRole(Enum):
    SUPER_ADMIN = "suer_admin"
    ADMIN = "admin"
    BUYER = "buyer"
    SOLVER = "solver"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    APPROVAL_PENDING = "approval_pending"


@dataclass
class User:
    id: int
    user_name : str
    email : str
    phone : str
    password: str
    user_status: UserStatus
    user_role: UserRole = UserRole.SOLVER
    uuid: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)


@dataclass
class UserRegistrationData:
    user_name : str
    email : str
    phone : str
    password: str
    user_role: UserRole = UserRole.SOLVER

@dataclass
class UserUpdateData:
    user_name : Optional[str] = None
    phone : Optional[str] = None
