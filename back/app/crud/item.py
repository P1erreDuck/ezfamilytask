from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from uuid import UUID
from datetime import datetime


async def create_item(session: AsyncSession, text: str):
    stmt = select(Item).where(Item.text == text)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise ValueError(f"Элемент с текстом '{text}' уже существует")

    db_item = Item(text=text)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def get_items(session: AsyncSession, limit: int):
    stmt = select(Item).order_by(Item.created_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_item(session: AsyncSession, item_id: UUID, new_text: str):
    stmt = select(Item).where(Item.text == new_text)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing and existing.id != item_id:
        raise ValueError(f"Элемент с текстом '{new_text}' уже существует")

    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if not item:
        return None

    item.text = new_text
    item.created_at = datetime.now()

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(session: AsyncSession, item_id: UUID):
    stmt = select(Item).where(Item.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if item:
        await session.delete(item)
        await session.commit()
        return True
    return False