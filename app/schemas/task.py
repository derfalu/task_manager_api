from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.tag import TagRead
import enum


class StatusEnum(str, enum.Enum):
    """
    Перечисление допустимых статусов задачи.
    """

    new = "new"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    """
    Схема для создания новой задачи.

    Поля:
    - title: название задачи (обязательное)
    - description: описание (необязательно)
    - status: статус задачи (по умолчанию — new)
    - due_date: срок выполнения
    - tags: список названий тегов
    """

    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.new
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """
    Схема для обновления задачи (все поля необязательные).

    Можно обновить:
    - заголовок
    - описание
    - статус
    - срок выполнения
    - список тегов
    """

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskRead(BaseModel):
    """
    Схема для чтения задачи из БД.

    Включает:
    - id: идентификатор задачи
    - title: заголовок
    - description: описание
    - status: текущий статус
    - due_date: срок выполнения
    - created_at: дата создания
    - tags: список тегов (объекты TagRead)
    - is_overdue: флаг просроченности
    """

    id: int
    title: str
    description: Optional[str]
    status: StatusEnum
    due_date: Optional[datetime]
    created_at: datetime
    tags: List[TagRead] = []
    is_overdue: bool

    model_config = {"from_attributes": True}
