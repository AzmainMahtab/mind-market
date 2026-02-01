from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from enum import Enum
from uuid import UUID, uuid7
from dataclasses import field

class Department(Enum):
    HR = "Human Resources"
    IT = "Information Technology"
    SALES = "Sales"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    MODARATER = "Modarater"

class AvailabilityStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

@dataclass
class Staff:
    id: int
    user_id: int
    full_name: str
    responsibilities: str
    hourly_rate: float
    rating: float
    uuid: UUID = field(default_factory=uuid7)
    department: Department = Department.MODARATER
    is_available: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    meta: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)

    
