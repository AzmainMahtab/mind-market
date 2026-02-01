from dataclasses import dataclass, field
from uuid import UUID, uuid7
from datetime import datetime, timezone
from typing import Optional, Any
from enum import Enum

class AvailabilityStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

@dataclass
class Solver:
    id: int
    user_id: int
    full_name: str
    bio: str
    hourly_rate: float
    experience_years: int
    rating: float
    total_projects: int
    completed_projects: int
    protfolio_url: str
    meta: dict[str, Any] = field(default_factory=dict)
    is_available: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    skills: list[str] = field(default_factory=list)
    uuid: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)
        
