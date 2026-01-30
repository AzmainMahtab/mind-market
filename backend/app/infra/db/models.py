from uuid import UUID
from datetime import datetime
from sqlalchemy import String, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

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
        SQLEnum(UserRole, name="user_role", create_type=True), 
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
