from fastapi import FastAPI
from routers import artworks
from database.database import init_db

app = FastAPI()

app.include_router(artworks.router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def home():
    return {"message": "Art Portfolio App is working"}