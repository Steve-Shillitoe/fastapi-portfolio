from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from routers import artworks
from database.database import init_db
from fastapi.staticfiles import StaticFiles
from fastapi import Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from models.artwork import Artwork
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
    db: AsyncSession = Depends(get_db),
):
    PAGE_SIZE = 3

    # Count total artworks
    count_result = await db.execute(
        select(func.count()).select_from(Artwork)
    )
    total = count_result.scalar_one()

    # Fetch paginated artworks
    result = await db.execute(
        select(Artwork)
        .order_by(desc(Artwork.id))
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
    )
    artworks = result.scalars().all()

    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "artworks": artworks,
            "page": page,
            "total_pages": total_pages,
        },
    )