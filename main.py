from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from routers import artworks
from database.database import init_db
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from models.artwork import Artwork


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
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Artwork))
    artworks = result.scalars().all()

    return templates.TemplateResponse(
        "gallery.html",
        {"request": request, "artworks": artworks},
    )