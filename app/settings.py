from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  computed_field

class Settings(BaseSettings):
    # --- Project Metadata --- #
    PROJECT_NAME: str = "Marketplace API"
    DEBUG: bool = False
    APP_PORT: int = 8080

    # --- PostgreSQL / SQLAlchemy --- #
    # Fallbacks are set for local development if .env is missing
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "marketplace"
    
    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Constructs the async database URL from components."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # --- Redis --- #
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0

    # --- NATS --- #
    NATS_URL: str = "nats://localhost:4222"

    # --- Security (ES256) --- #
    # These point to the certs folder we created in /backend/certs/
    # Make sure to generate keys beforehand
    AUTH_PRIVATE_KEY_PATH: str = "./certs/private.pem"
    AUTH_PUBLIC_KEY_PATH: str = "./certs/public.pem"
    AUTH_ALGORITHM: str = "ES256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pydantic configuration to read from .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

# Singleton instance
settings = Settings()
