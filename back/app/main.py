from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import items
import os

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app = FastAPI(
    title="EZ Family Task",
    description="Тестовое задание.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)