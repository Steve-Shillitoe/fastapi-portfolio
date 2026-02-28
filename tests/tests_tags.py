import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from services.tag_service import process_tags_fast
from models.tag import Tag
from sqlalchemy import select


@pytest.mark.asyncio
async def test_process_tags_fast_creates_tags(override_get_db):
    async for db in override_get_db():
        tags = await process_tags_fast(db, "oil, portrait, oil")
        await db.commit()

        result = await db.execute(select(Tag))
        stored_tags = result.scalars().all()

        assert len(stored_tags) == 2
        assert sorted([t.name for t in stored_tags]) == ["oil", "portrait"]