
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.session import get_async_session
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.crud.item import create_item, get_items, delete_item, update_item

router = APIRouter(prefix="/api/items", tags=["Элементы"])

@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый элемент",
    description="Создает новый элемент с переданным текстом. Текст должен быть уникальным и не длиннее 50 символов.",
    responses={
        201: {"description": "Элемент успешно создан"},
        400: {"description": "Текст пустой, слишком длинный или уже существует"},
    }
)
async def create_item_endpoint(
    item: ItemCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await create_item(session, item.text)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[ItemResponse],
    summary="Получить список элементов",
    description="Возвращает список последних элементов. Можно указать лимит (по умолчанию 20).",
    responses={
        200: {"description": "Успешный ответ со списком элементов"},
    }
)
async def get_items_endpoint(
    limit: int = Query(20, ge=1, le=100, description="Количество элементов (от 1 до 100)"),
    session: AsyncSession = Depends(get_async_session)
):
    return await get_items(session, limit)

@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Обновить элемент",
    description="Обновляет текст элемента по его ID. Дата создания обновляется.",
    responses={
        200: {"description": "Элемент успешно обновлен"},
        400: {"description": "Текст пустой, слишком длинный или уже существует"},
        404: {"description": "Элемент с указанным ID не найден"},
    }
)
async def update_item_endpoint(
    item_id: UUID,
    item: ItemUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        updated = await update_item(session, item_id, item.text)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Элемент не найден"
            )
        return updated
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить элемент",
    description="Удаляет элемент по его ID.",
    responses={
        204: {"description": "Элемент успешно удален"},
        404: {"description": "Элемент с указанным ID не найден"},
    }
)
async def delete_item_endpoint(
    item_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    deleted = await delete_item(session, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Элемент не найден"
        )
    return None
