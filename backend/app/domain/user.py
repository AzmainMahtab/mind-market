from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from dataclasses import dataclass, field
from datetime import datetime, timezone

class UserRole(Enum):
    ADMIN = "admin"
    BUYER = "buyer"
    SOLVER = "solver"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


@dataclass
class User:
    id: int
    user_name : str
    email : str
    phone : str
    user_role: UserRole
    user_status: UserStatus
    uuid: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)



