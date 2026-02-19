from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import items

app = FastAPI(
    title="EZ Family Task",
    description="""
    Тестовое задание
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://192.168.100.14:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
