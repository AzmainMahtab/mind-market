from dataclasses import dataclass, field
import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from datetime import datetime, timezone

class ProjectStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Project:
    id: int
    project_name: str
    project_description: str
    project_budget: float
    project_duration_days: int
    buyer_id: int
    solver_id: int
    uuid: UUID = field(default_factory=uuid7)
    project_status: ProjectStatus = ProjectStatus.PENDING
    solver_assiened_at: str = field(default="")
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)

