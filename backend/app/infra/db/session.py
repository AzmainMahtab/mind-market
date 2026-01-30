from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.settings import settings
from sqlalchemy import text

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
