from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import artworks
from database.database import init_db
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (optional cleanup)


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(artworks.router)


@app.get("/")
async def home():
    return {"message": "Art Portfolio App is working"}