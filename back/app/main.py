from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from back.app.api import items

app = FastAPI(
    title="EZ Family Task",
    description="""
    Тестовое задание.

    ## Возможности
    * **Создание** новых элементов
    * **Просмотр** списка элементов
    * **Обновление** существующих элементов
    * **Удаление** элементов

    Все текстовые поля проходят валидацию:
    * Не могут быть пустыми
    * Не длиннее 50 символов
    * Должны быть уникальными
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "tazetdinov",
        "email": "dtazetdinov1998@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://192.168.100.14:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
