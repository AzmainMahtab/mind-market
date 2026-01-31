from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid7
from datetime import datetime, timezone

class ProposalStatus(Enum):
    PENDING = "pending"  # Added pending as a logical starting state
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class Proposal:
    id: int
    project_id: int
    solver_id: int
    
    proposed_price: float 
    cover_letter: str
    
    # Identity and Status
    uuid: UUID = field(default_factory=uuid7)
    proposal_status: ProposalStatus = ProposalStatus.PENDING
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = field(default=None)
