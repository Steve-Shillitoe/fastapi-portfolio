"""
Database configuration module.

This module:
- Loads the database URL from environment variables
- Creates the asynchronous SQLAlchemy engine
- Provides an async session factory
- Defines the Base class for ORM models
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase


# Load environment variables from .env file
load_dotenv()


# Retrieve the database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")


# Create an asynchronous SQLAlchemy engine
# echo=True logs SQL statements (useful during development)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# Create a factory for asynchronous database sessions
# expire_on_commit=False prevents objects from being expired
# after commit, which avoids needing to refresh them manually
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# Base class for all ORM models
# All models will inherit from this class
class Base(DeclarativeBase):
    pass