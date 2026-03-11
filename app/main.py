"""
Главное приложение FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router

app = FastAPI(
    title="Yartumba API",
    description="Мебельная конфигураторная система",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "Yartumba API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
