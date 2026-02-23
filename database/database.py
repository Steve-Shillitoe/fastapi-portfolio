"""
Database configuration module.
"""

import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

 # Load environment variables from .env file, allowing overrides for development and testing.
 # This ensures that the DATABASE_URL can be set in the .env file and will be used by the application.
 # The override=True parameter allows environment variables to be overridden by those in the .env file,
 # which is useful for development and testing environments.
load_dotenv(override=True) 

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")


# Async engine is used to support non-blocking database I/O.
# This allows the application to handle concurrent requests efficiently.
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# Provides a request-scoped AsyncSession via FastAPI dependency injection.
# A new session is created for each request and automatically closed
# after the request completes, ensuring safe and clean DB usage.
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency-injected async database session.
    """
    async with AsyncSessionLocal() as session:
        yield session


# IMPORTANT: import models so SQLAlchemy knows about them
import models.artwork

async def init_db() -> None:
    """
    Create database tables.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)