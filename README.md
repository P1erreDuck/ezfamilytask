# EZ Family Task

**Backend:** FastAPI + PostgreSQL\
**Frontend:** Vue 3 + Pinia\
**Деплой:** Docker Compose

------------------------------------------------------------------------

## Быстрый старт

### Требования

- **Docker**
- **Docker Compose Plugin** (версия 2.0+)
- **Git**

------------------------------------------------------------------------

## Установка


git clone https://github.com/P1erreDuck/ezfamilytask.git

------------------------------------------------------------------------

Создайте файл `.env` в корне проекта и укажите:

    POSTGRES_USER=ваш_пользователь_бд
    POSTGRES_PASSWORD=ваш_пароль_бд
    POSTGRES_DB=название_бд
    POSTGRES_PORT=5432
    BACKEND_PORT=8000
    FRONTEND_PORT=5173
    VITE_API_URL=http://<IP_СЕРВЕРА>:8000
    CORS_ORIGINS=http://localhost:5173,http://<IP_СЕРВЕРА>:5173  # Адреса фронтенда

------------------------------------------------------------------------


sudo docker compose up --build


После запуска будут доступны:

-   Backend: http://localhost:8000
-   Frontend: http://localhost:5173

------------------------------------------------------------------------

## API Документация

Swagger: http://localhost:8000/docs

------------------------------------------------------------------------

## CRUD операции

POST     /api/items            Создать новый элемент
  
GET      /api/items            Получить список элементов
  
PUT      /api/items/{id}       Обновить элемент
  
DELETE   /api/items/{id}       Удалить элемент

------------------------------------------------------------------------

## Связь

Telegram: https://t.me/pd45000000
