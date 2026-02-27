"""
Artwork ORM model using SQLAlchemy 2.x style mappings.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from database.database import Base
from models.tag import artwork_tags
from sqlalchemy.orm import relationship
from typing import List,  TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.tag import Tag

class Artwork(Base):
    """
    ORM model representing an artwork record.
    """

    __tablename__ = "artworks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    image_filename: Mapped[str] = mapped_column(String(300), nullable=False)

    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    tags: Mapped[List["Tag"]] = relationship(
    secondary=artwork_tags,
    back_populates="artworks",
)

    @property
    def image_url(self) -> str:
        if not self.image_filename:
            return ""
        return f"/static/uploads/{self.image_filename}"