from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Default to a local SQLite file so tests run without an external DB.
    # This can be overridden with the environment variable `DATABASE_URL`.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./test.db"
    )

    class Config:
        env_file = ".env"


settings = Settings()