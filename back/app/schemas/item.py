from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID


class ItemCreate(BaseModel):
    text: str

    @field_validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Текст не может быть пустым')
        if len(v) > 50:
            raise ValueError('Текст не может быть длиннее 50 символов')
        return v.strip()


class ItemUpdate(BaseModel):
    text: str

    @field_validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Текст не может быть пустым')
        if len(v) > 50:
            raise ValueError('Текст не может быть длиннее 50 символов')
        return v.strip()


class ItemResponse(BaseModel):
    id: UUID
    text: str
    created_at: datetime

    class Config:
        from_attributes = True