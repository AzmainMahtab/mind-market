from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from datetime import datetime, timezone

class CompletionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REVISION_REQUESTED = "revision_requested"
    CANCELLED = "cancelled"

@dataclass
class ProjectCompletionRequest:
    id: int
    project_id: int
    completion_remark: str
    solver_rating: float   
    uuid: UUID = field(default_factory=uuid7)
    completion_status: CompletionStatus = CompletionStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)
