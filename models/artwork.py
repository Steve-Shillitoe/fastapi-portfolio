"""
Database ORM models for the art portfolio application.
"""

from sqlalchemy import Column, Integer, String, Text
from database import Base
from fastapi import settings

class Artwork(Base):
    """
    ORM model representing an artwork record.
    """

    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    image_filename = Column(String(300), nullable=False)
    comments = Column(Text, nullable=True)

    @property
    def image_path(self) -> str:
        """
        Returns the public URL path to the artwork image.
        """
        if self.image_filename:
            return f"/static/uploads/{self.image_filename}"

        return "/static/uploads/default.png"