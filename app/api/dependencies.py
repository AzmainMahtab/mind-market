from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.session import async_session_factory, ping_database
from app.secure.argon import ArgonHaser 
from app.infra.db.repo.user_repo import AlchemyUserRepository
from app.services.user_service import UserServiceImpl

async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_db_connection():
    "Check the database connection"
    return await ping_database()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserServiceImpl:
    user_repo = AlchemyUserRepository(db)
    hasher = ArgonHaser()
    return UserServiceImpl(user_repo, hasher)
