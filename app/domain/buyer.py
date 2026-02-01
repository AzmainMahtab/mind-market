from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import UUID, uuid7
from datetime import datetime, timezone
from typing import Optional

class HiringStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"

@dataclass
class Buyer:
    id: int
    user_id: int
    bio: str
    total_spent: float
    active_years: int
    rating: float
    total_projects: int
    completed_projects: int
    business_url: str
    meta: dict[str,Any] = field(default_factory=dict)
    is_hiring: HiringStatus = HiringStatus.OPEN
    uuid: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)


