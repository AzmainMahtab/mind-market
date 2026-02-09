from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.settings import settings
from app.infra.db.session import ping_database, engine

from app.api.v1.endpoints import user_endpoint

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the startup and shutdown of the application.
    """
    print(f" Initializing {settings.PROJECT_NAME}...")
    
    # Use  infra helper
    db_alive = await ping_database()
    
    if db_alive:
        print("Postgres 17 connection established.")
    else:
        print("UNABLE TO REACH DATABASE. !!!")
        print("Check your .env credentials and ensure the Postgres container is running.")

    yield # This is where the FastAPI app starts receiving traffic

    # --- SHUTDOWN --- #
    print("Shutting down application...")
    # Properly close all connections in the pool
    await engine.dispose()
    print("Database connection pool closed.")

# Initialize FastAPI with our lifespan manager
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Marketplace API with Hexagonal Architecture",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_endpoint.router)

@app.get("/health", tags=["System"])
async def health_check():
    """
    Check the status of the API and its connection to the database.
    """
    is_db_up = await ping_database()
    return {
        "status": "online" if is_db_up else "degraded",
        "database": "connected" if is_db_up else "disconnected",
        "version": app.version
    }
