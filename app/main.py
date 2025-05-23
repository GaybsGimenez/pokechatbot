from fastapi import FastAPI
from app.router import router

app = FastAPI(title="PokéChatBot")

app.include_router(router)