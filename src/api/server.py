from fastapi import FastAPI
from src.api.routes.chat import router as chat_router

app = FastAPI(
    title="Franquinelson API",
    description="API para interagir com o assistente Franquinelson",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/chat")
