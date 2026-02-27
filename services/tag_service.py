from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from models.tag import Tag


async def process_tags_fast(
    db: AsyncSession,
    tags_str: str | None,
):
    """
    High performance tag processor.

    - Fetches existing tags in bulk
    - Inserts missing tags in bulk
    - Returns list of Tag objects
    """

    if not tags_str:
        return []

    # Normalize tag names
    tag_names = list({
        t.strip().lower()
        for t in tags_str.split(",")
        if t.strip()
    })

    if not tag_names:
        return []

    # ------------------------------------------------
    # Step 1: Fetch existing tags in ONE query
    # ------------------------------------------------
    result = await db.execute(
        select(Tag).where(Tag.name.in_(tag_names))
    )

    existing_tags = {tag.name: tag for tag in result.scalars().all()}

    # ------------------------------------------------
    # Step 2: Determine missing tags
    # ------------------------------------------------
    missing_tag_names = [
        name
        for name in tag_names
        if name not in existing_tags
    ]

    # ------------------------------------------------
    # Step 3: Bulk insert missing tags (VERY FAST)
    # ------------------------------------------------
    if missing_tag_names:
        await db.execute(
            insert(Tag).values(
                [{"name": name} for name in missing_tag_names]
            )
        )

        await db.commit()

        # Reload newly created tags
        result = await db.execute(
            select(Tag).where(Tag.name.in_(tag_names))
        )

        tags = result.scalars().all()

    else:
        tags = list(existing_tags.values())

    return tags


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