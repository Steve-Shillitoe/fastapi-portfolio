"""
Artwork ORM model using SQLAlchemy 2.x style mappings.
"""

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from database.database import Base


class Artwork(Base):
    """
    ORM model representing an artwork record.
    """

    __tablename__ = "artworks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    image_filename: Mapped[str] = mapped_column(String(300), nullable=False)

    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)