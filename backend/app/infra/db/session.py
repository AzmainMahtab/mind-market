from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.settings import settings
from sqlalchemy import text
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from uuid import UUID
import uuid_utils



# Use the pre-computed URL from settings class
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL, 
    echo=settings.DEBUG  # Only log SQL in debug mode
)

async_session_factory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession  # Explicitly tell it to use AsyncSession
)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass


class CommonMixin:
    """Standard columns for all models."""
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Indexed UUID7
    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        unique=True, 
        index=True, 
        nullable=False, 
        default=uuid_utils.uuid7,
        server_default=func.gen_random_uuid()
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Soft Delete - Indexed 
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        index=True, 
        nullable=True
    )


async def get_db():
    """Dependency for FastAPI routes to inject a database session"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def ping_database() -> bool:
    """Verifies the DB connection."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database Ping Failed: {e}")
        return False
