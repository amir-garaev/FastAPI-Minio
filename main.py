from fastapi import FastAPI
from app_meme.routers import meme

app = FastAPI()

app.include_router(meme.router, prefix="/memes", tags=["memes"])
