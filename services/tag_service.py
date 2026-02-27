from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.tag import Tag


async def process_tags(
    db: AsyncSession,
    tags_str: str | None,
):
    """
    Process comma-separated tag string.
    Creates tags if they do not exist.
    Returns list of Tag objects.
    """

    tag_objects = []

    if not tags_str:
        return tag_objects

    tag_names = [
        t.strip().lower()
        for t in tags_str.split(",")
        if t.strip()
    ]

    for tag_name in tag_names:
        result = await db.execute(
            select(Tag).where(Tag.name == tag_name)
        )

        tag = result.scalar_one_or_none()

        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)

        tag_objects.append(tag)

    return tag_objects