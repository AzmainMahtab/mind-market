from app.infra.db.session import async_session_factory, ping_database

async def get_db():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_db_connection():
    "Check the database connection"
    return await ping_database()
