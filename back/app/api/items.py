from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from back.app.db.session import get_async_session
from back.app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from back.app.crud.item import create_item, get_items, delete_item, update_item

router = APIRouter(prefix="/api/items", tags=["items"])

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
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

@router.get("/", response_model=List[ItemResponse])
async def get_items_endpoint(
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session)
):
    return await get_items(session, limit)

@router.put("/{item_id}", response_model=ItemResponse)
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

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
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