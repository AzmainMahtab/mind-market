from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from datetime import datetime, timezone

class BuyerFeedback(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REVISION_REQUESTED = "revision_requested"
    REJECTED = "rejected"

@dataclass
class TaskSubmission:
    id: int
    task_id: int
    file_path: str
    version: int
    uuid: UUID = field(default_factory=uuid7)
    buyer_feedback: BuyerFeedback = BuyerFeedback.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)
