from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Art Portfolio App is working"}