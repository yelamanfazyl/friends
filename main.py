from config import get_settings
from fastapi import FastAPI
import models  # type: ignore

settings = get_settings()

app = FastAPI(title="Friends API")

@app.get("/")
async def root():
    return {"message": "Hello nfactorial!"}