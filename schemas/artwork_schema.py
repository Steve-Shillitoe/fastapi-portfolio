"""
Pydantic schemas for artwork validation and serialization.
"""

from typing import Optional
from pydantic import BaseModel


class ArtworkCreate(BaseModel):
    """
    Schema used when creating a new artwork.
    """

    title: str
    comments: Optional[str] = None


class ArtworkResponse(BaseModel):
    """
    Schema used when returning artwork data to frontend.
    """

    id: int
    title: str
    image_filename: str
    comments: Optional[str]
    image_url: str
    tags: list[str]
    class Config:
        from_attributes = True


class ArtworkUpdate(BaseModel):
    title: str
    comments: str | None = None
    tags: str | None = None       