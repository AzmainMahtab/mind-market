from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from datetime import datetime, timezone

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"

@dataclass
class Task:
    id: int
    project_id: int
    task_description: str
    uuid: UUID = field(default_factory=uuid7)
    task_status: TaskStatus = TaskStatus.TODO
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)
