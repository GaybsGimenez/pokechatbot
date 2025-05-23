# from fastapi import FastAPI
# from app.router import router

# app = FastAPI(title="PokéChatBot")

# app.include_router(router)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.router import router
from app.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa banco de dados ao iniciar a aplicação
    init_db()
    yield
    # Aqui você pode colocar lógica de encerramento se quiser (ex: fechar conexões)

app = FastAPI(
    title="PokéChatBot",
    lifespan=lifespan
)

app.include_router(router)


