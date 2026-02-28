from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, Query
from routers import artworks
from database.database import init_db
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from models.artwork import Artwork
from models.tag import Tag
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (optional cleanup)

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(artworks.router)


@app.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request,
    page: int = Query(1, ge=1),
    tag: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    PAGE_SIZE = 3

    # Base query
    query = select(Artwork).order_by(desc(Artwork.id))
    count_query = select(func.count()).select_from(Artwork)

    # If tag filter exists
    if tag:
        query = (
            query
            .join(Artwork.tags)
            .where(Tag.name.ilike(f"%{tag.lower()}%"))
        )

        count_query = (
            select(func.count())
            .select_from(Artwork)
            .join(Artwork.tags)
            .where(Tag.name.ilike(f"%{tag.lower()}%"))
        )

    # Get total count
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # Apply pagination
    result = await db.execute(
        query
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
    )

    artworks = result.scalars().unique().all()

    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "artworks": artworks,
            "page": page,
            "total_pages": total_pages,
            "tag": tag,
        },
    )