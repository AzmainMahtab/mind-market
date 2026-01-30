from uuid import UUID
from datetime import datetime
from sqlalchemy import ARRAY, JSON, String, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from typing import Any

from app.domain.solver import AvailabilityStatus
from app.infra.db.session import Base
from app.domain.user import UserRole, UserStatus

class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), unique=True, index=True, nullable=False)
    
    user_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    user_role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", create_type=True, default=UserRole.SOLVER),
        nullable=False
    )
    user_status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus, name="user_status", create_type=True), 
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )


class SolverTable(Base):
    __tablename__ = "solvers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), unique=True, index=True, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    hourly_rate: Mapped[float] = mapped_column(nullable=False)
    experience_years: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False, default=0.0)

    total_projects: Mapped[int] = mapped_column(nullable=False, default=0)
    completed_projects: Mapped[int] = mapped_column(nullable=False, default=0)
    is_available: Mapped[AvailabilityStatus] = mapped_column(
        SQLEnum(
            AvailabilityStatus, 
            name="availability_status", 
            create_type=True, 
            default=AvailabilityStatus.AVAILABLE
        ),
        nullable=False
    )

    meta: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        server_default='{}'
    )
    
    skills: Mapped[list[str]] = mapped_column(
        ARRAY(String(50)),
        nullable=False,
        server_default='{}'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )


