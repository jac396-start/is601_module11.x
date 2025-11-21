# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from .config import settings


def get_engine(database_url: str = settings.DATABASE_URL):
    """
    Create and return a new SQLAlchemy engine.

    Automatically adds SQLite-specific connect args when the URL
    starts with "sqlite:" to ensure compatibility with multiple
    threads/sessions during testing.
    """
    try:
        connect_args = {}
        if database_url.startswith("sqlite"):
            # For SQLite, allow connections across threads (useful for tests)
            connect_args = {"check_same_thread": False}
        engine = create_engine(database_url, echo=True, connect_args=connect_args)
        return engine
    except SQLAlchemyError as e:
        print(f"Error creating engine: {e}")
        raise


def get_sessionmaker(engine):
    """
    Create and return a new sessionmaker bound to `engine`.
    """
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


# Initialize engine and SessionLocal using the factory functions
engine = get_engine()
SessionLocal = get_sessionmaker(engine)

# Base declarative class that our models will inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session for FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
