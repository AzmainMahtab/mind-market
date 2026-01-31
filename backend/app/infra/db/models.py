from sqlalchemy import ARRAY, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Any

from app.domain.solver import AvailabilityStatus
from app.infra.db.session import Base, CommonMixin
from app.domain.user import UserRole, UserStatus
from app.domain.buyer import HiringStatus

class UserTable(CommonMixin, Base):
    __tablename__ = "users"

    
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



class SolverTable(CommonMixin ,Base):
    __tablename__ = "solvers"

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
        JSONB,
        nullable=False,
        server_default='{}'
    )
    
    skills: Mapped[list[str]] = mapped_column(
        ARRAY(String(50)),
        nullable=False,
        server_default='{}'
    )


class BuyerTable(CommonMixin, Base):
    __tablename__ = "buyers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    business_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    total_spent: Mapped[float] = mapped_column(nullable=False, default=0.0)
    active_years: Mapped[int] = mapped_column(nullable=False, default=0)
    rating: Mapped[float] = mapped_column(nullable=False, default=5.0)

    total_projects: Mapped[int] = mapped_column(nullable=False, default=0)
    completed_projects: Mapped[int] = mapped_column(nullable=False, default=0)

    is_hiring: Mapped[HiringStatus] = mapped_column(
        SQLEnum(HiringStatus, name="hiring_status", create_type=True),
        nullable=False,
        default=HiringStatus.OPEN
    )

    meta: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        server_default='{}'
    )
