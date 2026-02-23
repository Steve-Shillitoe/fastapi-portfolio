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


load_dotenv()

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