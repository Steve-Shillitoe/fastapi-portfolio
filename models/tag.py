from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base
from typing import List,  TYPE_CHECKING
#if TYPE_CHECKING:
 #   from models.artwork import Artwork

artwork_tags = Table(
    "artwork_tags",
    Base.metadata,
    Column("artwork_id", ForeignKey("artworks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    artworks: Mapped[List["Artwork"]] = relationship(
        back_populates="tags",
        secondary=artwork_tags,
    )